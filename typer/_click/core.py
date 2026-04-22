import enum
import inspect
import os
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Mapping, MutableMapping, Sequence
from contextlib import AbstractContextManager, ExitStack, contextmanager
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    NoReturn,
    TypeVar,
    Union,
    cast,
    overload,
)

from . import types
from .exceptions import (
    Abort,
    BadParameter,
    Exit,
    MissingParameter,
    NoArgsIsHelpError,
    UsageError,
)
from .formatting import HelpFormatter
from .globals import pop_context, push_context
from .parser import _OptionParser
from .termui import style
from .utils import (
    echo,
    make_default_short_help,
)

if TYPE_CHECKING:
    from ..core import TyperOption
    from .shell_completion import CompletionItem

F = TypeVar("F", bound="Callable[..., Any]")
V = TypeVar("V")


def _complete_visible_commands(
    ctx: "Context", incomplete: str
) -> Iterator[tuple[str, "Command"]]:
    """List all the subcommands of a group that start with the
    incomplete value and aren't hidden.
    """
    # avoid circular imports
    from ..core import TyperGroup

    multi = cast(TyperGroup, ctx.command)

    for name in multi.list_commands(ctx):
        if name.startswith(incomplete):
            command = multi.get_command(ctx, name)

            if command is not None and not command.hidden:
                yield name, command


@contextmanager
def augment_usage_errors(
    ctx: "Context", param: Union["Parameter", None] = None
) -> Iterator[None]:
    """Context manager that attaches extra information to exceptions."""
    try:
        yield
    except BadParameter as e:
        if e.ctx is None:
            e.ctx = ctx
        if param is not None and e.param is None:
            e.param = param
        raise
    except UsageError as e:  # pragma: no cover
        if e.ctx is None:
            e.ctx = ctx
        raise


def iter_params_for_processing(
    invocation_order: Sequence["Parameter"],
    declaration_order: Sequence["Parameter"],
) -> list["Parameter"]:
    """Returns all declared parameters in the order they should be processed.

    The declared parameters are re-shuffled depending on the order in which
    they were invoked, as well as the eagerness of each parameters.

    The invocation order takes precedence over the declaration order. I.e. the
    order in which the user provided them to the CLI is respected.

    This behavior and its effect on callback evaluation is detailed at:
    https://click.palletsprojects.com/en/stable/advanced/#callback-evaluation-order
    """

    def sort_key(item: Parameter) -> tuple[bool, float]:
        try:
            idx: float = invocation_order.index(item)
        except ValueError:
            idx = float("inf")

        return not item.is_eager, idx

    return sorted(declaration_order, key=sort_key)


class ParameterSource(enum.Enum):
    """This is an `Enum` that indicates the source of a
    parameter's value.
    """

    COMMANDLINE = enum.auto()
    """The value was provided by the command line args."""
    ENVIRONMENT = enum.auto()
    """The value was provided with an environment variable."""
    DEFAULT = enum.auto()
    """Used the default specified by the parameter."""
    DEFAULT_MAP = enum.auto()
    """Used a default provided by `Context.default_map`."""
    PROMPT = enum.auto()
    """Used a prompt to confirm a default or provide a value."""


class Context:
    """The context is a special internal object that holds state relevant
    for the script execution at every single level.  It's normally invisible
    to commands unless they opt-in to getting access to it.

    The context is useful as it can pass internal objects around and can
    control special execution features such as reading data from
    environment variables.

    A context can be used as context manager in which case it will call
    `close` on teardown.
    """

    formatter_class: type[HelpFormatter] = HelpFormatter

    def __init__(
        self,
        command: "Command",
        parent: Union["Context", None] = None,
        info_name: str | None = None,
        obj: Any | None = None,
        auto_envvar_prefix: str | None = None,
        default_map: MutableMapping[str, Any] | None = None,
        terminal_width: int | None = None,
        max_content_width: int | None = None,
        resilient_parsing: bool = False,
        allow_extra_args: bool | None = None,
        allow_interspersed_args: bool | None = None,
        ignore_unknown_options: bool | None = None,
        help_option_names: list[str] | None = None,
        token_normalize_func: Callable[[str], str] | None = None,
        color: bool | None = None,
        show_default: bool | None = None,
    ) -> None:
        self.parent = parent
        self.command = command
        self.info_name = info_name
        # Map of parameter names to their parsed values.
        self.params: dict[str, Any] = {}
        # the leftover arguments.
        self.args: list[str] = []
        # protected arguments. used to implement nested parsing.
        self._protected_args: list[str] = []
        # the collected prefixes of the command's options.
        self._opt_prefixes: set[str] = set(parent._opt_prefixes) if parent else set()

        if obj is None and parent is not None:
            obj = parent.obj

        self.obj: Any = obj
        self._meta: dict[str, Any] = getattr(parent, "meta", {})

        # A dictionary (-like object) with defaults for parameters.
        if (
            default_map is None
            and info_name is not None
            and parent is not None
            and parent.default_map is not None
        ):
            default_map = parent.default_map.get(info_name)

        self.default_map: MutableMapping[str, Any] | None = default_map

        # This flag indicates if a subcommand is going to be executed.
        self.invoked_subcommand: str | None = None

        if terminal_width is None and parent is not None:
            terminal_width = parent.terminal_width

        # The width of the terminal (None is autodetection).
        self.terminal_width: int | None = terminal_width

        if max_content_width is None and parent is not None:
            max_content_width = parent.max_content_width

        self.max_content_width: int | None = max_content_width

        if allow_extra_args is None:
            allow_extra_args = command.allow_extra_args

        self.allow_extra_args = allow_extra_args

        if allow_interspersed_args is None:
            allow_interspersed_args = command.allow_interspersed_args

        self.allow_interspersed_args: bool = allow_interspersed_args

        if ignore_unknown_options is None:
            ignore_unknown_options = command.ignore_unknown_options

        self.ignore_unknown_options: bool = ignore_unknown_options

        if help_option_names is None:
            if parent is not None:
                help_option_names = parent.help_option_names
            else:
                help_option_names = ["--help"]

        self.help_option_names: list[str] = help_option_names

        if token_normalize_func is None and parent is not None:
            token_normalize_func = parent.token_normalize_func

        # An optional normalization function for tokens. (options, choices, commands etc.)
        self.token_normalize_func: Callable[[str], str] | None = token_normalize_func

        # Indicates if resilient parsing is enabled.
        self.resilient_parsing: bool = resilient_parsing

        # If there is no envvar prefix yet, but the parent has one and
        # the command on this level has a name, we can expand the envvar
        # prefix automatically.
        if auto_envvar_prefix is None:
            if (
                parent is not None
                and parent.auto_envvar_prefix is not None
                and self.info_name is not None
            ):
                auto_envvar_prefix = (
                    f"{parent.auto_envvar_prefix}_{self.info_name.upper()}"
                )
        else:
            auto_envvar_prefix = auto_envvar_prefix.upper()

        if auto_envvar_prefix is not None:
            auto_envvar_prefix = auto_envvar_prefix.replace("-", "_")

        self.auto_envvar_prefix: str | None = auto_envvar_prefix

        if color is None and parent is not None:
            color = parent.color

        # Controls if styling output is wanted or not.
        self.color: bool | None = color

        if show_default is None and parent is not None:
            show_default = parent.show_default

        # Show option default values when formatting help text.
        self.show_default: bool | None = show_default

        self._close_callbacks: list[Callable[[], Any]] = []
        self._depth = 0
        self._parameter_source: dict[str, ParameterSource] = {}
        self._exit_stack = ExitStack()

    def __enter__(self) -> "Context":
        self._depth += 1
        push_context(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        self._depth -= 1
        exit_result: bool | None = None
        if self._depth == 0:
            exit_result = self._close_with_exception_info(exc_type, exc_value, tb)
        pop_context()

        return exit_result

    @contextmanager
    def scope(self, cleanup: bool = True) -> Iterator["Context"]:
        """This helper method can be used with the context object to promote
        it to the current thread local (see `get_current_context`).
        The default behavior of this is to invoke the cleanup functions which
        can be disabled by setting `cleanup` to `False`.  The cleanup
        functions are typically used for things such as closing file handles.

        If the cleanup is intended the context object can also be directly
        used as a context manager.
        """
        if not cleanup:
            self._depth += 1
        try:
            with self as rv:
                yield rv
        finally:
            if not cleanup:
                self._depth -= 1

    @property
    def meta(self) -> dict[str, Any]:
        """This is a dictionary which is shared with all the contexts
        that are nested.  It exists so that click utilities can store some
        state here if they need to.  It is however the responsibility of
        that code to manage this dictionary well.

        The keys are supposed to be unique dotted strings.  For instance
        module paths are a good choice for it.  What is stored in there is
        irrelevant for the operation of click.  However what is important is
        that code that places data here adheres to the general semantics of
        the system.
        """
        return self._meta

    def make_formatter(self) -> HelpFormatter:
        """Creates the HelpFormatter for the help and
        usage output.
        """
        return self.formatter_class(
            width=self.terminal_width, max_width=self.max_content_width
        )

    def with_resource(self, context_manager: AbstractContextManager[V]) -> V:
        """Register a resource as if it were used in a ``with``
        statement. The resource will be cleaned up when the context is
        popped.

        Uses `contextlib.ExitStack.enter_context`. It calls the
        resource's ``__enter__()`` method and returns the result. When
        the context is popped, it closes the stack, which calls the
        resource's ``__exit__()`` method.

        To register a cleanup function for something that isn't a
        context manager, use `call_on_close`. Or use something
        from `contextlib` to turn it into a context manager first.
        """
        return self._exit_stack.enter_context(context_manager)

    def call_on_close(self, f: Callable[..., Any]) -> Callable[..., Any]:
        """Register a function to be called when the context tears down.

        This can be used to close resources opened during the script
        execution. Resources that support Python's context manager
        protocol which would be used in a ``with`` statement should be
        registered with `with_resource` instead.
        """
        return self._exit_stack.callback(f)

    def close(self) -> None:
        """Invoke all close callbacks registered with `call_on_close`,
        and exit all context managers entered with `with_resource`.
        """
        self._close_with_exception_info(None, None, None)

    def _close_with_exception_info(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        """Unwind the exit stack by calling its `__exit__` providing the exception
        information to allow for exception handling by the various resources registered
        using `with_resource`
        """
        exit_result = self._exit_stack.__exit__(exc_type, exc_value, tb)
        # In case the context is reused, create a new exit stack.
        self._exit_stack = ExitStack()

        return exit_result

    @property
    def command_path(self) -> str:
        """The computed command path.  This is used for the ``usage``
        information on the help page.  It's automatically created by
        combining the info names of the chain of contexts to the root.
        """
        rv = ""
        if self.info_name is not None:
            rv = self.info_name
        if self.parent is not None:
            parent_command_path = [self.parent.command_path]

            if isinstance(self.parent.command, Command):
                for param in self.parent.command.get_params(self):
                    parent_command_path.extend(param.get_usage_pieces(self))

            rv = f"{' '.join(parent_command_path)} {rv}"
        return rv.lstrip()

    def find_root(self) -> "Context":
        """Finds the outermost context."""
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def find_object(self, object_type: type[V]) -> V | None:
        """Finds the closest object of a given type."""
        node: Context | None = self

        while node is not None:
            if isinstance(node.obj, object_type):
                return node.obj

            node = node.parent

        return None

    def ensure_object(self, object_type: type[V]) -> V:
        """Like `find_object` but sets the innermost object to a
        new instance of `object_type` if it does not exist.
        """
        rv = self.find_object(object_type)
        if rv is None:
            self.obj = rv = object_type()
        return rv

    @overload
    def lookup_default(self, name: str, call: Literal[True] = True) -> Any | None: ...

    @overload
    def lookup_default(
        self, name: str, call: Literal[False] = ...
    ) -> Any | Callable[[], Any] | None: ...

    def lookup_default(self, name: str, call: bool = True) -> Any | None:
        """Get the default for a parameter from `default_map`."""
        if self.default_map is not None:
            value = self.default_map.get(name)

            if call and callable(value):
                return value()

            return value

        return None

    def fail(self, message: str) -> NoReturn:
        """Aborts the execution of the program with a specific error
        message.
        """
        raise UsageError(message, self)

    def abort(self) -> NoReturn:
        """Aborts the script."""
        raise Abort()

    def exit(self, code: int = 0) -> NoReturn:
        """Exits the application with a given exit code."""
        self.close()
        raise Exit(code)

    def get_usage(self) -> str:
        """Helper method to get formatted usage string for the current
        context and command.
        """
        return self.command.get_usage(self)

    def get_help(self) -> str:
        """Helper method to get formatted help page for the current
        context and command.
        """
        return self.command.get_help(self)

    def invoke(self, callback: Callable[..., V], /, *args: Any, **kwargs: Any) -> V:
        """Invokes a command callback in exactly the way it expects.  There
        are two ways to invoke this method:

        1.  the first argument can be a callback and all other arguments and
            keyword arguments are forwarded directly to the function.
        2.  the first argument is a click command object.  In that case all
            arguments are forwarded as well but proper click parameters
            (options and click arguments) must be keyword arguments and Click
            will fill in defaults.
        """
        ctx = self

        with augment_usage_errors(self):
            with ctx:
                return callback(*args, **kwargs)

    def set_parameter_source(self, name: str, source: ParameterSource) -> None:
        """Set the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.
        """
        self._parameter_source[name] = source

    def get_parameter_source(self, name: str) -> ParameterSource | None:
        """Get the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.

        This can be useful for determining when a user specified a value
        on the command line that is the same as the default value. It
        will be `ParameterSource.DEFAULT` only if the
        value was actually taken from the default.
        """
        return self._parameter_source.get(name)


class Command(ABC):
    """Commands are the basic building block of command line interfaces in
    Click.  A basic command handles command line parsing and might dispatch
    more parsing to commands nested below it.
    """

    context_class: type[Context] = Context
    allow_extra_args = False
    allow_interspersed_args = True
    ignore_unknown_options = False

    def __init__(
        self,
        name: str | None,
        context_settings: MutableMapping[str, Any] | None = None,
        callback: Callable[..., Any] | None = None,
        params: list["Parameter"] | None = None,
        help: str | None = None,
        epilog: str | None = None,
        short_help: str | None = None,
        options_metavar: str | None = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool | str = False,
    ) -> None:
        self.name = name

        if context_settings is None:
            context_settings = {}

        self.context_settings: MutableMapping[str, Any] = context_settings

        self.callback = callback
        self.params: list[Parameter] = params or []
        self.help = help
        self.epilog = epilog
        self.options_metavar = options_metavar
        self.short_help = short_help
        self.add_help_option = add_help_option
        self._help_option = None
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def get_usage(self, ctx: Context) -> str:
        """Formats the usage line into a string and returns it."""
        formatter = ctx.make_formatter()
        self.format_usage(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def get_params(self, ctx: Context) -> list["Parameter"]:
        params = self.params
        help_option = self.get_help_option(ctx)

        if help_option is not None:
            params = [*params, help_option]

        return params

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes the usage line into the formatter."""
        pieces = self.collect_usage_pieces(ctx)
        formatter.write_usage(ctx.command_path, " ".join(pieces))

    def collect_usage_pieces(self, ctx: Context) -> list[str]:
        """Returns all the pieces that go into the usage line and returns
        it as a list of strings.
        """
        rv = [self.options_metavar] if self.options_metavar else []

        for param in self.get_params(ctx):
            rv.extend(param.get_usage_pieces(ctx))

        return rv

    def get_help_option_names(self, ctx: Context) -> list[str]:
        """Returns the names for the help option."""
        all_names = set(ctx.help_option_names)
        for param in self.params:
            all_names.difference_update(param.opts)
            all_names.difference_update(param.secondary_opts)
        return list(all_names)

    def get_help_option(self, ctx: Context) -> Union["TyperOption", None]:
        """Returns the help option object."""
        help_option_names = self.get_help_option_names(ctx)

        if not help_option_names or not self.add_help_option:
            return None

        # Cache the help option object in private _help_option attribute to
        # avoid creating it multiple times. Not doing this will break the
        # callback odering by iter_params_for_processing(), which relies on
        # object comparison.
        if self._help_option is None:
            # Avoid circular import.
            from .decorators import help_option

            # Apply help_option decorator and pop resulting option
            help_option(help_option_names)(self)
            self._help_option = self.params.pop()  # type: ignore[assignment]

        return self._help_option

    def make_parser(self, ctx: Context) -> _OptionParser:
        """Creates the underlying option parser for this command."""
        parser = _OptionParser(ctx)
        for param in self.get_params(ctx):
            param.add_to_parser(parser, ctx)
        return parser

    def get_help(self, ctx: Context) -> str:
        """Formats the help into a string and returns it."""
        formatter = ctx.make_formatter()
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def get_short_help_str(self, limit: int = 45) -> str:
        """Gets short help for the command or makes it by shortening the
        long help string.
        """
        if self.short_help:
            text = inspect.cleandoc(self.short_help)
        elif self.help:
            text = make_default_short_help(self.help, limit)
        else:
            text = ""

        if self.deprecated:
            deprecated_message = (
                f"(DEPRECATED: {self.deprecated})"
                if isinstance(self.deprecated, str)
                else "(DEPRECATED)"
            )
            text = f"{text} {deprecated_message}"

        return text.strip()

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes the help into the formatter if it exists."""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes the help text to the formatter if it exists."""
        if self.help is not None:
            # truncate the help text to the first form feed
            text = inspect.cleandoc(self.help).partition("\f")[0]
        else:
            text = ""

        if self.deprecated:
            deprecated_message = (
                f"(DEPRECATED: {self.deprecated})"
                if isinstance(self.deprecated, str)
                else "(DEPRECATED)"
            )
            text = f"{text} {deprecated_message}"

        if text:
            formatter.write_paragraph()

            with formatter.indentation():
                formatter.write_text(text)

    @abstractmethod
    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass  # pragma: no cover

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes the epilog into the formatter if it exists."""
        if self.epilog:
            epilog = inspect.cleandoc(self.epilog)
            formatter.write_paragraph()

            with formatter.indentation():
                formatter.write_text(epilog)

    def make_context(
        self,
        info_name: str | None,
        args: list[str],
        parent: Context | None = None,
        **extra: Any,
    ) -> Context:
        """This function when given an info name and arguments will kick
        off the parsing and create a new `Context`.  It does not
        invoke the actual command callback though.

        To quickly customize the context class used without overriding
        this method, set the `context_class` attribute.
        """
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value

        ctx = self.context_class(self, info_name=info_name, parent=parent, **extra)

        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)
        return ctx

    def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            raise NoArgsIsHelpError(ctx)  # pragma: no cover

        parser = self.make_parser(ctx)
        opts, args, param_order = parser.parse_args(args=args)

        for param in iter_params_for_processing(param_order, self.get_params(ctx)):
            _, args = param.handle_parse_result(ctx, opts, args)

        if args and not ctx.allow_extra_args and not ctx.resilient_parsing:
            ctx.fail(f"Got unexpected extra argument(s) ({' '.join(map(str, args))})")

        ctx.args = args
        ctx._opt_prefixes.update(parser._opt_prefixes)
        return args

    def invoke(self, ctx: Context) -> Any:
        """Given a context, this invokes the attached callback (if it exists)
        in the right way.
        """
        if self.deprecated:
            extra_message = (
                f" {self.deprecated}" if isinstance(self.deprecated, str) else ""
            )
            message = f"DeprecationWarning: The command {self.name!r} is deprecated.{extra_message}"
            echo(style(message, fg="red"), err=True)

        if self.callback is not None:
            return ctx.invoke(self.callback, **ctx.params)

    def shell_complete(self, ctx: Context, incomplete: str) -> list["CompletionItem"]:
        """Return a list of completions for the incomplete value. Looks
        at the names of options and chained multi-commands.

        Any command could be part of a chained multi-command, so sibling
        commands are valid at any point during command completion.
        """
        # avoid circular imports
        from .shell_completion import CompletionItem

        results: list[CompletionItem] = []

        if incomplete and not incomplete[0].isalnum():
            # avoid circular imports
            from ..core import TyperOption

            for param in self.get_params(ctx):
                if (
                    not isinstance(param, TyperOption)
                    or param.hidden
                    or (
                        not param.multiple
                        and ctx.get_parameter_source(param.name)  # type: ignore
                        is ParameterSource.COMMANDLINE
                    )
                ):
                    continue

                results.extend(
                    CompletionItem(name, help=param.help)
                    for name in [*param.opts, *param.secondary_opts]
                    if name.startswith(incomplete)
                )

        return results

    @abstractmethod
    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        pass  # pragma: no cover

    @abstractmethod
    def _main_shell_completion(
        self,
        ctx_args: MutableMapping[str, Any],
        prog_name: str,
        complete_var: str | None = None,
    ) -> None:
        pass  # pragma: no cover

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Alias for self.main"""
        return self.main(*args, **kwargs)


class Parameter(ABC):
    r"""A parameter to a command comes in two versions: they are either
    `Option`\s or `Argument`\s.

    Some settings are supported by both options and arguments.
    """

    param_type_name = "parameter"

    def __init__(
        self,
        param_decls: Sequence[str] | None = None,
        type: types.ParamType | Any | None = None,
        required: bool = False,
        default: Any | Callable[[], Any] | None = None,
        callback: Callable[[Context, "Parameter", Any], Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | Sequence[str] | None = None,
        shell_complete: Callable[
            [Context, "Parameter", str], list["CompletionItem"] | list[str]
        ]
        | None = None,
    ) -> None:
        self.name: str | None
        self.opts: list[str]
        self.secondary_opts: list[str]
        self.name, self.opts, self.secondary_opts = self._parse_decls(
            param_decls or (), expose_value
        )
        self.type: types.ParamType = types.convert_type(type, default)

        # Default nargs to what the type tells us if we have that
        # information available.
        if nargs is None:
            if self.type.is_composite:
                nargs = self.type.arity
            else:
                nargs = 1

        self.required = required
        self.callback = callback
        self.nargs = nargs
        self.multiple = multiple
        self.expose_value = expose_value
        self.default: Any | Callable[[], Any] | None = default
        self.is_eager = is_eager
        self.metavar = metavar
        self.envvar = envvar
        self._custom_shell_complete = shell_complete

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    @abstractmethod
    def _parse_decls(
        self, decls: Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        pass  # pragma: no cover

    @property
    def human_readable_name(self) -> str:
        """Returns the human readable name of this parameter.  This is the
        same as the name for options, but the metavar for arguments.
        """
        assert self.name is not None, "self.name should be set"
        return self.name

    def make_metavar(self, ctx: Context) -> str:
        if self.metavar is not None:
            return self.metavar

        metavar = self.type.get_metavar(param=self, ctx=ctx)

        if metavar is None:
            metavar = self.type.name.upper()

        if self.nargs != 1:
            metavar += "..."

        return metavar

    @overload
    def get_default(self, ctx: Context, call: Literal[True] = True) -> Any | None: ...

    @overload
    def get_default(
        self, ctx: Context, call: bool = ...
    ) -> Any | Callable[[], Any] | None: ...

    def get_default(
        self, ctx: Context, call: bool = True
    ) -> Any | Callable[[], Any] | None:
        """Get the default for the parameter"""
        value = ctx.lookup_default(self.name, call=False)  # type: ignore

        if value is None:
            value = self.default

        if call and callable(value):
            value = value()

        return value

    @abstractmethod
    def add_to_parser(self, parser: _OptionParser, ctx: Context) -> None:
        pass  # pragma: no cover

    def consume_value(
        self, ctx: Context, opts: Mapping[str, Any]
    ) -> tuple[Any, ParameterSource]:
        value = opts.get(self.name)  # type: ignore
        source = ParameterSource.COMMANDLINE

        if value is None:
            value = self.value_from_envvar(ctx)
            source = ParameterSource.ENVIRONMENT

        if value is None:
            value = ctx.lookup_default(self.name)  # type: ignore
            source = ParameterSource.DEFAULT_MAP

        if value is None:
            value = self.get_default(ctx)
            source = ParameterSource.DEFAULT

        return value, source

    def type_cast_value(self, ctx: Context, value: Any) -> Any:
        """Convert and validate a value against the parameter's
        `type`, `multiple`, and `nargs`.
        """
        if value is None:
            return () if self.multiple or self.nargs == -1 else None

        def check_iter(value: Any) -> Iterator[Any]:
            assert not isinstance(value, str)
            return iter(value)

        # Define the conversion function based on nargs and type.
        if self.nargs == 1 or self.type.is_composite:

            def convert(value: Any) -> Any:
                return self.type(value, param=self, ctx=ctx)

        elif self.nargs == -1:

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                return tuple(self.type(x, self, ctx) for x in check_iter(value))

        # TODO: evaluate whether we need to keep this in Typer
        else:  # nargs > 1

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                value = tuple(check_iter(value))

                if len(value) != self.nargs:
                    raise BadParameter(
                        f"Takes {self.nargs} values but {len(value)} given.",
                        ctx=ctx,
                        param=self,
                    )

                return tuple(self.type(x, self, ctx) for x in value)

        if self.multiple:
            return tuple(convert(x) for x in check_iter(value))

        return convert(value)

    @abstractmethod
    def value_is_missing(self, value: Any) -> bool:
        pass  # pragma: no cover

    def process_value(self, ctx: Context, value: Any) -> Any:
        """Process the value of this parameter"""
        value = self.type_cast_value(ctx, value)

        if self.required and self.value_is_missing(value):
            raise MissingParameter(ctx=ctx, param=self)

        if self.callback is not None:
            value = self.callback(ctx, self, value)

        return value

    def resolve_envvar_value(self, ctx: Context) -> str | None:
        """Returns the value found in the environment variable(s) attached to this
        parameter.

        Environment variables values are `always returned as strings
        <https://docs.python.org/3/library/os.html#os.environ>`_.

        This method returns ``None`` if:

        - the `envvar` property is not set on `Parameter`,
        - the environment variable is not found in the environment,
        - the variable is found in the environment but its value is empty (i.e. the
          environment variable is present but has an empty string).

        If `envvar` is setup with multiple environment variables,
        then only the first non-empty value is returned.
        """
        if self.envvar is None:
            return None

        if isinstance(self.envvar, str):
            rv = os.environ.get(self.envvar)

            if rv:
                return rv
        else:
            for envvar in self.envvar:
                rv = os.environ.get(envvar)

                # Return the first non-empty value of the list of environment variables.
                if rv:
                    return rv
                # Else, absence of value is interpreted as an environment variable that
                # is not set, so proceed to the next one.

        return None

    def value_from_envvar(self, ctx: Context) -> str | Sequence[str] | None:
        """Process the raw environment variable string for this parameter.

        Returns the string as-is or splits it into a sequence of strings if the
        parameter is expecting multiple values (i.e. its `nargs` property is set
        to a value other than ``1``).
        """
        rv: Any | None = self.resolve_envvar_value(ctx)

        if rv is not None and self.nargs != 1:
            rv = self.type.split_envvar_value(rv)

        return rv

    def handle_parse_result(
        self, ctx: Context, opts: Mapping[str, Any], args: list[str]
    ) -> tuple[Any, list[str]]:
        """Process the value produced by the parser from user input.

        Always process the value through the Parameter's `type`, wherever it
        comes from.

        If the parameter is deprecated, this method warn the user about it. But only if
        the value has been explicitly set by the user (and as such, is not coming from
        a default).
        """
        with augment_usage_errors(ctx, param=self):
            value, source = self.consume_value(ctx, opts)

            ctx.set_parameter_source(self.name, source)  # type: ignore

            # Process the value through the parameter's type.
            try:
                value = self.process_value(ctx, value)
            except Exception:
                if not ctx.resilient_parsing:
                    raise
                value = None

        if self.expose_value:
            ctx.params[self.name] = value  # type: ignore

        return value, args

    @abstractmethod
    def get_help_record(self, ctx: Context) -> tuple[str, str] | None:
        pass  # pragma: no cover

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return []

    def get_error_hint(self, ctx: Context) -> str:
        """Get a stringified version of the param for use in error messages to
        indicate which param caused the error.
        """
        hint_list = self.opts or [self.human_readable_name]
        return " / ".join(f"'{x}'" for x in hint_list)

    def shell_complete(self, ctx: Context, incomplete: str) -> list["CompletionItem"]:
        """Return a list of completions for the incomplete value. If a
        ``shell_complete`` function was given during init, it is used.
        Otherwise, the `type` `ParamType.shell_complete` function is used.
        """
        if self._custom_shell_complete is not None:
            results = self._custom_shell_complete(ctx, self, incomplete)

            if results and isinstance(results[0], str):
                from .shell_completion import CompletionItem

                results = [CompletionItem(c) for c in results]

            return cast("list[CompletionItem]", results)

        return self.type.shell_complete(ctx, self, incomplete)
