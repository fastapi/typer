import re
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from typing import Any, ClassVar, TypeVar

from .core import Command, Context, Parameter, ParameterSource


class CompletionItem:
    """Represents a completion value and metadata about the value. The
    default metadata is ``type`` to indicate special shell handling,
    and ``help`` if a shell supports showing a help string next to the
    value.

    Arbitrary parameters can be passed when creating the object, and
    accessed using ``item.attr``. If an attribute wasn't passed,
    accessing it returns ``None``.
    """

    __slots__ = ("value", "type", "help", "_info")

    def __init__(
        self,
        value: Any,
        type: str = "plain",
        help: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.value: Any = value
        self.type: str = type
        self.help: str | None = help
        self._info = kwargs

    def __getattr__(self, name: str) -> Any:
        return self._info.get(name)


class ShellComplete(ABC):
    """Base class for providing shell completion support. A subclass for
    a given shell will override attributes and methods to implement the
    completion instructions (``source`` and ``complete``).
    """

    name: ClassVar[str]
    """Name to register the shell as with `add_completion_class`.
    This is used in completion instructions (``{name}_source`` and
    ``{name}_complete``).
    """

    source_template: ClassVar[str]
    """Completion script template formatted by `source`. This must
    be provided by subclasses.
    """

    def __init__(
        self,
        cli: Command,
        ctx_args: MutableMapping[str, Any],
        prog_name: str,
        complete_var: str,
    ) -> None:
        self.cli = cli
        self.ctx_args = ctx_args
        self.prog_name = prog_name
        self.complete_var = complete_var

    @property
    def func_name(self) -> str:
        """The name of the shell function defined by the completion
        script.
        """
        safe_name = re.sub(r"\W*", "", self.prog_name.replace("-", "_"), flags=re.ASCII)
        return f"_{safe_name}_completion"

    @abstractmethod
    def source_vars(self) -> dict[str, Any]:
        """Vars for formatting `source_template`."""
        pass  # pragma: no cover

    def source(self) -> str:
        """Produce the shell script that defines the completion
        function. By default this ``%``-style formats
        `source_template` with the dict returned by `source_vars`.
        """
        return self.source_template % self.source_vars()

    @abstractmethod
    def get_completion_args(self) -> tuple[list[str], str]:
        """Use the env vars defined by the shell script to return a
        tuple of ``args, incomplete``. This must be implemented by
        subclasses.
        """
        pass  # pragma: no cover

    def get_completions(self, args: list[str], incomplete: str) -> list[CompletionItem]:
        """Determine the context and last complete command or parameter
        from the complete args. Call that object's ``shell_complete``
        method to get the completions for the incomplete value.
        """
        ctx = _resolve_context(self.cli, self.ctx_args, self.prog_name, args)
        obj, incomplete = _resolve_incomplete(ctx, args, incomplete)
        return obj.shell_complete(ctx, incomplete)

    @abstractmethod
    def format_completion(self, item: CompletionItem) -> str:
        """Format a completion item into the form recognized by the
        shell script. This must be implemented by subclasses.
        """
        pass  # pragma: no cover

    def complete(self) -> str:
        """Produce the completion data to send back to the shell.

        By default this calls `get_completion_args`, gets the
        completions, then calls `format_completion` for each
        completion.
        """
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\n".join(out)


ShellCompleteType = TypeVar("ShellCompleteType", bound="type[ShellComplete]")


_available_shells: dict[str, type[ShellComplete]] = {}


def add_completion_class(cls: ShellCompleteType, name: str) -> ShellCompleteType:
    """Register a `ShellComplete` subclass under the given name.
    The name will be provided by the completion instruction environment
    variable during completion.
    """
    _available_shells[name] = cls

    return cls


def get_completion_class(shell: str) -> type[ShellComplete] | None:
    """Look up a registered `ShellComplete` subclass by the name
    provided by the completion instruction environment variable. If the
    name isn't registered, returns ``None``.
    """
    return _available_shells.get(shell)


def split_arg_string(string: str) -> list[str]:
    """Split an argument string as with `shlex.split`, but don't
    fail if the string is incomplete. Ignores a missing closing quote or
    incomplete escape sequence and uses the partial token as-is.
    """
    import shlex

    lex = shlex.shlex(string, posix=True)
    lex.whitespace_split = True
    lex.commenters = ""
    out = []

    try:
        for token in lex:
            out.append(token)
    except ValueError:
        # Raised when end-of-string is reached in an invalid state. Use
        # the partial token as-is. The quote or escape character is in
        # lex.state, not lex.token.
        out.append(lex.token)

    return out


def _is_incomplete_argument(ctx: Context, param: Parameter) -> bool:
    """Determine if the given parameter is an argument that can still
    accept values.
    """
    # avoid circular imports
    from ..core import TyperArgument

    if not isinstance(param, TyperArgument):
        return False

    assert param.name is not None
    # Will be None if expose_value is False.
    value = ctx.params.get(param.name)
    return (
        param.nargs == -1
        or ctx.get_parameter_source(param.name) is not ParameterSource.COMMANDLINE
        or (
            param.nargs > 1
            and isinstance(value, (tuple, list))
            and len(value) < param.nargs
        )
    )


def _start_of_option(ctx: Context, value: str) -> bool:
    """Check if the value looks like the start of an option."""
    if not value:
        return False

    c = value[0]
    return c in ctx._opt_prefixes


def _is_incomplete_option(ctx: Context, args: list[str], param: Parameter) -> bool:
    """Determine if the given parameter is an option that needs a value."""
    # avoid circular imports
    from ..core import TyperOption

    if not isinstance(param, TyperOption):
        return False

    if param.is_flag or param.count:
        return False

    last_option = None

    for index, arg in enumerate(reversed(args)):
        if index + 1 > param.nargs:
            break

        if _start_of_option(ctx, arg):
            last_option = arg
            break

    return last_option is not None and last_option in param.opts


def _resolve_context(
    cli: Command,
    ctx_args: MutableMapping[str, Any],
    prog_name: str,
    args: list[str],
) -> Context:
    """Produce the context hierarchy starting with the command and
    traversing the complete arguments. This only follows the commands,
    it doesn't trigger input prompts or callbacks.
    """
    # avoid circular imports
    from ..core import TyperGroup

    ctx_args["resilient_parsing"] = True
    with cli.make_context(prog_name, args.copy(), **ctx_args) as ctx:
        args = ctx._protected_args + ctx.args

        while args:
            command = ctx.command

            if isinstance(command, TyperGroup):
                # if not command.chain:
                name, cmd, args = command.resolve_command(ctx, args)

                if cmd is None:
                    return ctx

                with cmd.make_context(
                    name, args, parent=ctx, resilient_parsing=True
                ) as sub_ctx:
                    ctx = sub_ctx
                    args = ctx._protected_args + ctx.args
            else:
                break

    return ctx


def _resolve_incomplete(
    ctx: Context, args: list[str], incomplete: str
) -> tuple[Command | Parameter, str]:
    """Find the Click object that will handle the completion of the
    incomplete value. Return the object and the incomplete value.
    """
    # Different shells treat an "=" between a long option name and
    # value differently. Might keep the value joined, return the "="
    # as a separate item, or return the split name and value. Always
    # split and discard the "=" to make completion easier.
    if incomplete == "=":
        incomplete = ""
    elif "=" in incomplete and _start_of_option(ctx, incomplete):
        name, _, incomplete = incomplete.partition("=")
        args.append(name)

    # The "--" marker tells Click to stop treating values as options
    # even if they start with the option character. If it hasn't been
    # given and the incomplete arg looks like an option, the current
    # command will provide option name completions.
    if "--" not in args and _start_of_option(ctx, incomplete):
        return ctx.command, incomplete

    params = ctx.command.get_params(ctx)

    # If the last complete arg is an option name with an incomplete
    # value, the option will provide value completions.
    for param in params:
        if _is_incomplete_option(ctx, args, param):
            return param, incomplete

    # It's not an option name or value. The first argument without a
    # parsed value will provide value completions.
    for param in params:
        if _is_incomplete_argument(ctx, param):
            return param, incomplete

    # There were no unparsed arguments, the command may be a group that
    # will provide command name completions.
    return ctx.command, incomplete
