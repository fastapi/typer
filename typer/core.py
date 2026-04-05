from __future__ import annotations

import errno
import inspect
import os
import sys
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Mapping, MutableMapping, Sequence
from difflib import get_close_matches
from enum import Enum
from gettext import gettext as _
from typing import (
    Any,
    TextIO,
    TypeVar,
    cast,
    overload,
)

from . import _click, echo
from ._click import make_str
from ._typing import Literal
from .context import Context, augment_usage_errors
from .utils import parse_boolean_env_var

MarkupMode = Literal["markdown", "rich", None]
MARKUP_MODE_KEY = "TYPER_RICH_MARKUP_MODE"

HAS_RICH = parse_boolean_env_var(os.getenv("TYPER_USE_RICH"), default=True)

if HAS_RICH:
    DEFAULT_MARKUP_MODE: MarkupMode = "rich"
else:
    DEFAULT_MARKUP_MODE = None

F = TypeVar("F", bound="Callable[..., Any]")


# Copy from _click.parser._split_opt
def _split_opt(opt: str) -> tuple[str, str]:
    first = opt[:1]
    if first.isalnum():
        return "", opt
    if opt[1:2] == first:
        return opt[:2], opt[2:]
    return first, opt[1:]


def _typer_param_setup_autocompletion_compat(
    self: Parameter,
    *,
    autocompletion: Callable[[Context, list[str], str], list[tuple[str, str] | str]]
    | None = None,
) -> None:
    if self._custom_shell_complete is not None:
        import warnings

        warnings.warn(
            "In Typer, only the parameter 'autocompletion' is supported. "
            "The support for 'shell_complete' is deprecated and will be removed in upcoming versions. ",
            DeprecationWarning,
            stacklevel=2,
        )

    if autocompletion is not None:

        def compat_autocompletion(
            ctx: Context, param: Parameter, incomplete: str
        ) -> list[_click.shell_completion.CompletionItem]:
            out = []

            assert autocompletion is not None
            for c in autocompletion(ctx, [], incomplete):
                if isinstance(c, tuple):
                    use_completion = _click.CompletionItem(c[0], help=c[1])
                else:
                    assert isinstance(c, str)
                    use_completion = _click.CompletionItem(c)

                if use_completion.value.startswith(incomplete):
                    out.append(use_completion)

            return out

        self._custom_shell_complete = compat_autocompletion


def _get_default_string(
    obj: TyperArgument | TyperOption,
    *,
    ctx: Context,
    show_default_is_str: bool,
    default_value: list[Any] | tuple[Any, ...] | str | Callable[..., Any] | Any,
) -> str:
    # Extracted from _click.core.Option.get_help_record() to be reused by
    # rich_utils avoiding RegEx hacks
    if show_default_is_str:
        default_string = f"({obj.show_default})"
    elif isinstance(default_value, (list, tuple)):
        default_string = ", ".join(
            _get_default_string(
                obj, ctx=ctx, show_default_is_str=show_default_is_str, default_value=d
            )
            for d in default_value
        )
    elif isinstance(default_value, Enum):
        default_string = str(default_value.value)
    elif inspect.isfunction(default_value):
        default_string = _("(dynamic)")
    elif isinstance(obj, TyperOption) and obj.is_bool_flag and obj.secondary_opts:
        # For boolean flags that have distinct True/False opts,
        # use the opt without prefix instead of the value.
        # Typer override, original commented
        # default_string = _click.parser.split_opt(
        #     (self.opts if self.default else self.secondary_opts)[0]
        # )[1]
        if obj.default:
            if obj.opts:
                default_string = _split_opt(obj.opts[0])[1]
            else:
                default_string = str(default_value)
        else:
            default_string = _split_opt(obj.secondary_opts[0])[1]
        # Typer override end
    elif (
        isinstance(obj, TyperOption)
        and obj.is_bool_flag
        and not obj.secondary_opts
        and not default_value
    ):
        default_string = ""
    else:
        default_string = str(default_value)
    return default_string


def _extract_default_help_str(
    obj: TyperArgument | TyperOption, *, ctx: Context
) -> Any | Callable[[], Any] | None:
    # Extracted from _click.core.Option.get_help_record() to be reused by
    # rich_utils avoiding RegEx hacks
    # Temporarily enable resilient parsing to avoid type casting
    # failing for the default. Might be possible to extend this to
    # help formatting in general.
    resilient = ctx.resilient_parsing
    ctx.resilient_parsing = True

    try:
        default_value = obj.get_default(ctx, call=False)
    finally:
        ctx.resilient_parsing = resilient
    return default_value


def _main(
    self: TyperCommand,
    *,
    args: Sequence[str] | None = None,
    prog_name: str | None = None,
    complete_var: str | None = None,
    standalone_mode: bool = True,
    windows_expand_args: bool = True,
    rich_markup_mode: MarkupMode = DEFAULT_MARKUP_MODE,
    **extra: Any,
) -> Any:
    # Typer override, duplicated from _click.main() to handle custom rich exceptions
    # Verify that the environment is configured correctly, or reject
    # further execution to avoid a broken script.
    if args is None:
        args = sys.argv[1:]

        # Covered in Click tests
        if os.name == "nt" and windows_expand_args:  # pragma: no cover
            args = _click.utils._expand_args(args)
    else:
        args = list(args)

    if prog_name is None:
        prog_name = _click.utils._detect_program_name()

    # Process shell completion requests and exit early.
    self._main_shell_completion(extra, prog_name, complete_var)

    try:
        try:
            with self.make_context(prog_name, args, **extra) as ctx:
                rv = self.invoke(ctx)
                if not standalone_mode:
                    return rv
                # it's not safe to `ctx.exit(rv)` here!
                # note that `rv` may actually contain data like "1" which
                # has obvious effects
                # more subtle case: `rv=[None, None]` can come out of
                # chained commands which all returned `None` -- so it's not
                # even always obvious that `rv` indicates success/failure
                # by its truthiness/falsiness
                ctx.exit()
        except EOFError as e:
            _click.echo(file=sys.stderr)
            raise _click.Abort() from e
        except KeyboardInterrupt as e:
            raise _click.exceptions.Exit(130) from e
        except _click.ClickException as e:
            if not standalone_mode:
                raise
            # Typer override
            if HAS_RICH and rich_markup_mode is not None:
                from . import rich_utils

                rich_utils.rich_format_error(e)
            else:
                e.show()
            # Typer override end
            sys.exit(e.exit_code)
        except OSError as e:
            if e.errno == errno.EPIPE:
                sys.stdout = cast(TextIO, _click.utils.PacifyFlushWrapper(sys.stdout))
                sys.stderr = cast(TextIO, _click.utils.PacifyFlushWrapper(sys.stderr))
                sys.exit(1)
            else:
                raise
    except _click.exceptions.Exit as e:
        if standalone_mode:
            sys.exit(e.exit_code)
        else:
            # in non-standalone mode, return the exit code
            # note that this is only reached if `self.invoke` above raises
            # an Exit explicitly -- thus bypassing the check there which
            # would return its result
            # the results of non-standalone execution may therefore be
            # somewhat ambiguous: if there are codepaths which lead to
            # `ctx.exit(1)` and to `return 1`, the caller won't be able to
            # tell the difference between the two
            return e.exit_code
    except _click.Abort:
        if not standalone_mode:
            raise
        # Typer override
        if HAS_RICH and rich_markup_mode is not None:
            from . import rich_utils

            rich_utils.rich_abort_error()
        else:
            _click.echo(_("Aborted!"), file=sys.stderr)
        # Typer override end
        sys.exit(1)


def _check_iter(value: Any) -> Iterator[Any]:
    """Check if the value is iterable but not a string. Raises a type
    error, or return an iterator over the value.
    """
    if isinstance(value, str):
        raise TypeError

    return iter(value)


class Parameter(ABC):
    """A parameter is either an option or an argument.
    Some functionality is specific to either of the two,
    so this abstract class bundles what is supported for both.
    """

    param_type_name = "parameter"

    def __init__(
        self,
        param_decls: Sequence[str] | None = None,
        type: _click.ParamType | Any | None = None,
        required: bool = False,
        default: Any | Callable[[], Any] | None = _click.UNSET,
        callback: Callable[[Context, Parameter, Any], Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | Sequence[str] | None = None,
        shell_complete: Callable[
            [Context, Parameter, str], list[_click.CompletionItem] | list[str]
        ]
        | None = None,
    ) -> None:
        self.name: str | None
        self.opts: list[str]
        self.secondary_opts: list[str]
        self.name, self.opts, self.secondary_opts = self._parse_decls(
            param_decls or (), expose_value
        )
        self.type: _click.ParamType = _click.convert_type(type, default)

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
    ) -> tuple[str | None, list[str], list[str]]: ...

    @property
    def human_readable_name(self) -> str:
        """Returns the human readable name of this parameter.  This is the
        same as the name for options, but the metavar for arguments.
        """
        return self.name  # type: ignore

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
        """Get the default for the parameter."""
        value = ctx.lookup_default(self.name, call=False)  # type: ignore

        if value is _click.UNSET:
            value = self.default

        if call and callable(value):
            value = value()

        return value

    @abstractmethod
    def add_to_parser(self, parser: _click._OptionParser, ctx: Context) -> None: ...

    def consume_value(
        self, ctx: Context, opts: Mapping[str, Any]
    ) -> tuple[Any, _click.ParameterSource]:
        """Returns the parameter value produced by the parser."""
        # Collect from the parse the value passed by the user to the CLI.
        value = opts.get(self.name, _click.UNSET)  # type: ignore
        # If the value is set, it means it was sourced from the command line by the
        # parser, otherwise it left unset by default.
        source = (
            _click.ParameterSource.COMMANDLINE
            if value is not _click.UNSET
            else _click.ParameterSource.DEFAULT
        )

        if value is _click.UNSET:
            envvar_value = self.value_from_envvar(ctx)
            if envvar_value is not None:
                value = envvar_value
                source = _click.ParameterSource.ENVIRONMENT

        if value is _click.UNSET:
            default_map_value = ctx.lookup_default(self.name)  # type: ignore
            if default_map_value is not _click.UNSET:
                value = default_map_value
                source = _click.ParameterSource.DEFAULT_MAP

        if value is _click.UNSET:
            default_value = self.get_default(ctx)
            if default_value is not _click.UNSET:
                value = default_value
                source = _click.ParameterSource.DEFAULT

        return value, source

    def type_cast_value(self, ctx: Context, value: Any) -> Any:
        """Convert and validate a value against the parameter's
        :attr:`type`, :attr:`multiple`, and :attr:`nargs`.
        """
        if value is None:
            if self.multiple or self.nargs == -1:
                return ()
            else:
                return value

        def check_iter(value: Any) -> Iterator[Any]:
            try:
                return _check_iter(value)
            except TypeError:
                # This should only happen when passing in args manually,
                # the parser should construct an iterable when parsing
                # the command line.
                raise _click.BadParameter(
                    _("Value must be an iterable."), ctx=ctx, param=self
                ) from None

        # Define the conversion function based on nargs and type.

        if self.nargs == 1 or self.type.is_composite:

            def convert(value: Any) -> Any:
                return self.type(value, param=self, ctx=ctx)

        elif self.nargs == -1:

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                return tuple(self.type(x, self, ctx) for x in check_iter(value))

        # TODO: remove or test
        else:  # nargs > 1

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                value = tuple(check_iter(value))

                if len(value) != self.nargs:
                    raise _click.BadParameter(
                        f"Takes {self.nargs} values but {len(value)} were given.",
                        ctx=ctx,
                        param=self,
                    )

                return tuple(self.type(x, self, ctx) for x in value)

        if self.multiple:
            return tuple(convert(x) for x in check_iter(value))

        return convert(value)

    @abstractmethod
    def value_is_missing(self, value: Any) -> bool: ...

    def process_value(self, ctx: Context, value: Any) -> Any:
        """Process the value of this parameter:

        1. Type cast the value
        2. Check if the value is missing
        3. If a `callback` is set, call it to have the value replaced by the
           result of the callback. If the value was not set, the callback receive
           ``None``. This keep the legacy behavior as it was before the introduction of
           the :attr:`UNSET` sentinel.
        """
        # shelter `type_cast_value` from ever seeing an `UNSET` value by handling the
        # cases in which `UNSET` gets special treatment explicitly at this layer
        #
        # Refs:
        # https://github.com/pallets/click/issues/3069
        if value is _click.UNSET:
            if self.multiple or self.nargs == -1:
                value = ()
        else:
            value = self.type_cast_value(ctx, value)

        if self.required and self.value_is_missing(value):
            raise _click.MissingParameter(ctx=ctx, param=self)

        if self.callback is not None:
            # Legacy case: UNSET is not exposed directly to the callback, but converted
            # to None.
            if value is _click.UNSET:
                value = None

            # Search for parameters with UNSET values in the context.
            unset_keys = {k: None for k, v in ctx.params.items() if v is _click.UNSET}
            # No UNSET values, call the callback as usual.
            if not unset_keys:
                value = self.callback(ctx, self, value)

            # Legacy case: provide a temporarily manipulated context to the callback
            # to hide UNSET values as None.
            #
            # Refs:
            # https://github.com/pallets/click/issues/3136
            # https://github.com/pallets/click/pull/3137
            else:
                # Add another layer to the context stack to clearly hint that the
                # context is temporarily modified.
                with ctx:
                    # Update the context parameters to replace UNSET with None.
                    ctx.params.update(unset_keys)
                    # Feed these fake context parameters to the callback.
                    value = self.callback(ctx, self, value)
                    # Restore the UNSET values in the context parameters.
                    ctx.params.update(
                        {
                            k: _click.UNSET
                            for k in unset_keys
                            # Only restore keys that are present and still None, in case
                            # the callback modified other parameters.
                            if k in ctx.params and ctx.params[k] is None
                        }
                    )

        return value

    def resolve_envvar_value(self, ctx: Context) -> str | None:
        """Returns the value found in the environment variable(s) attached to this
        parameter.

        Environment variables values are `always returned as strings
        <https://docs.python.org/3/library/os.html#os.environ>`_.

        This method returns ``None`` if:

        - the :attr:`envvar` property is not set on the :class:`Parameter`,
        - the environment variable is not found in the environment,
        - the variable is found in the environment but its value is empty (i.e. the
          environment variable is present but has an empty string).

        If :attr:`envvar` is setup with multiple environment variables,
        then only the first non-empty value is returned.

        .. caution::

            The raw value extracted from the environment is not normalized and is
            returned as-is. Any normalization or reconciliation is performed later by
            the :class:`Parameter`'s :attr:`type`.
        """
        if not self.envvar:
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
        parameter is expecting multiple values (i.e. its :attr:`nargs` property is set
        to a value other than ``1``).
        """
        rv = self.resolve_envvar_value(ctx)

        if rv is not None and self.nargs != 1:
            return self.type.split_envvar_value(rv)

        return rv

    def handle_parse_result(
        self, ctx: Context, opts: Mapping[str, Any], args: list[str]
    ) -> tuple[Any, list[str]]:
        """Process the value produced by the parser from user input.

        Always process the value through the Parameter's :attr:`type`, wherever it
        comes from.
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
                # In resilient parsing mode, we do not want to fail the command if the
                # value is incompatible with the parameter type, so we reset the value
                # to UNSET, which will be interpreted as a missing value.
                value = _click.UNSET

        # Add parameter's value to the context.
        if (
            self.expose_value
            # We skip adding the value if it was previously set by another parameter
            # targeting the same variable name. This prevents parameters competing for
            # the same name to override each other.
            and (self.name not in ctx.params or ctx.params[self.name] is _click.UNSET)
        ):
            # Click is logically enforcing that the name is None if the parameter is
            # not to be exposed. We still assert it here to please the type checker.
            assert self.name is not None, (
                f"{self!r} parameter's name should not be None when exposing value."
            )
            ctx.params[self.name] = value

        return value, args

    @abstractmethod
    def get_help_record(self, ctx: Context) -> tuple[str, str] | None: ...

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return []

    def get_error_hint(self, ctx: Context) -> str:
        """Get a stringified version of the param for use in error messages to
        indicate which param caused the error.
        """
        hint_list = self.opts or [self.human_readable_name]
        return " / ".join(f"'{x}'" for x in hint_list)

    def shell_complete(
        self, ctx: Context, incomplete: str
    ) -> list[_click.CompletionItem]:
        """Return a list of completions for the incomplete value."""
        if self._custom_shell_complete is not None:
            results = self._custom_shell_complete(ctx, self, incomplete)

            if results and isinstance(results[0], str):
                results = [_click.CompletionItem(c) for c in results]

            return cast("list[_click.CompletionItem]", results)

        return self.type.shell_complete(ctx, self, incomplete)


class TyperArgument(Parameter):
    param_type_name = "argument"

    def __init__(
        self,
        *,
        # Parameter
        param_decls: list[str],
        type: Any | None = None,
        required: bool | None = None,
        default: Any | None = None,
        callback: Callable[..., Any] | None = None,
        nargs: int | None = None,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | list[str] | None = None,
        # Note that shell_complete is not fully supported and will be removed in future versions
        # TODO: Remove shell_complete in a future version (after 0.16.0)
        shell_complete: Callable[
            [Context, Parameter, str],
            list[_click.shell_completion.CompletionItem] | list[str],
        ]
        | None = None,
        autocompletion: Callable[..., Any] | None = None,
        # TyperArgument
        show_default: bool | str = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        help: str | None = None,
        hidden: bool = False,
        # Rich settings
        rich_help_panel: str | None = None,
    ):
        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar
        self.hidden = hidden
        self.rich_help_panel = rich_help_panel

        # Auto-detect the requirement status of the argument if not explicitly set.
        # TODO: Doesn't hit coverage -> investigate, maybe remove
        if required is None:
            # The argument gets automatically required if it has no explicit default
            # value set and is setup to match at least one value.
            if default is _click.UNSET:
                if nargs is not None:
                    required = nargs > 0
                else:
                    required = True
            # If the argument has a default value, it is not required.
            else:
                required = False
        super().__init__(
            param_decls=param_decls,
            type=type,
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
        )
        _typer_param_setup_autocompletion_compat(self, autocompletion=autocompletion)

    @property
    def human_readable_name(self) -> str:
        if self.metavar is not None:
            return self.metavar
        return self.name.upper()  # type: ignore

    def _get_default_string(
        self,
        *,
        ctx: Context,
        show_default_is_str: bool,
        default_value: list[Any] | tuple[Any, ...] | str | Callable[..., Any] | Any,
    ) -> str:
        return _get_default_string(
            self,
            ctx=ctx,
            show_default_is_str=show_default_is_str,
            default_value=default_value,
        )

    def _extract_default_help_str(
        self, *, ctx: Context
    ) -> Any | Callable[[], Any] | None:
        return _extract_default_help_str(self, ctx=ctx)

    def get_help_record(self, ctx: Context) -> tuple[str, str] | None:
        # Modified version of _click.core.Option.get_help_record()
        # to support Arguments
        if self.hidden:
            return None
        name = self.make_metavar(ctx=ctx)
        help = self.help or ""
        extra = []
        if self.show_envvar:
            envvar = self.envvar
            # allow_from_autoenv is currently not supported in Typer for CLI Arguments
            if envvar is not None:
                var_str = (
                    ", ".join(str(d) for d in envvar)
                    if isinstance(envvar, (list, tuple))
                    else envvar
                )
                extra.append(f"env var: {var_str}")

        # Typer override:
        # Extracted to _extract_default_help_str() to allow re-using it in rich_utils
        default_value = self._extract_default_help_str(ctx=ctx)
        # Typer override end

        show_default_is_str = isinstance(self.show_default, str)

        if show_default_is_str or (
            default_value is not None and (self.show_default or ctx.show_default)
        ):
            # Typer override:
            # Extracted to _get_default_string() to allow re-using it in rich_utils
            default_string = self._get_default_string(
                ctx=ctx,
                show_default_is_str=show_default_is_str,
                default_value=default_value,
            )
            # Typer override end
            if default_string:
                extra.append(_("default: {default}").format(default=default_string))
        if self.required:
            extra.append(_("required"))
        if extra:
            extra_str = "; ".join(extra)
            extra_str = f"[{extra_str}]"
            rich_markup_mode = None
            if hasattr(ctx, "obj") and isinstance(ctx.obj, dict):
                rich_markup_mode = ctx.obj.get(MARKUP_MODE_KEY, None)
            if HAS_RICH and rich_markup_mode == "rich":
                # This is needed for when we want to export to HTML
                from . import rich_utils

                extra_str = rich_utils.escape_before_html_export(extra_str)

            help = f"{help}  {extra_str}" if help else f"{extra_str}"
        return name, help

    def make_metavar(self, ctx: Context | None = None) -> str:
        # Modified version of _click.core.Argument.make_metavar()
        # to include Argument name
        if self.metavar is not None:
            var = self.metavar
            if not self.required and not var.startswith("["):
                var = f"[{var}]"
            return var
        var = (self.name or "").upper()
        if not self.required:
            var = f"[{var}]"
        type_var = self.type.get_metavar(self, ctx=ctx) if ctx else None
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var

    def value_is_missing(self, value: Any) -> bool:
        return _value_is_missing(self, value)

    def _parse_decls(
        self, decls: Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        if not decls:
            if not expose_value:
                return None, [], []
            raise TypeError("Argument is marked as exposed, but does not have a name.")
        if len(decls) == 1:
            name = arg = decls[0]
            name = name.replace("-", "_").lower()
        else:
            raise TypeError(
                "Arguments take exactly one parameter declaration, got"
                f" {len(decls)}: {decls}."
            )
        return name, [arg], []

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return [self.make_metavar(ctx)]

    def get_error_hint(self, ctx: Context) -> str:
        return f"'{self.make_metavar(ctx)}'"

    def add_to_parser(self, parser: _click._OptionParser, ctx: Context) -> None:
        parser.add_argument(dest=self.name, nargs=self.nargs, obj=self)


class TyperOption(Parameter):
    param_type_name = "option"

    def __init__(
        self,
        *,
        # Parameter
        param_decls: list[str],
        type: _click.types.ParamType | Any | None = None,
        required: bool | None = None,
        default: Any | None = None,
        callback: Callable[..., Any] | None = None,
        nargs: int | None = None,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | list[str] | None = None,
        # Note that shell_complete is not fully supported and will be removed in future versions
        # TODO: Remove shell_complete in a future version (after 0.16.0)
        shell_complete: Callable[
            [Context, Parameter, str],
            list[_click.shell_completion.CompletionItem] | list[str],
        ]
        | None = None,
        autocompletion: Callable[..., Any] | None = None,
        # Option
        show_default: bool | str = False,
        prompt: bool | str = False,
        confirmation_prompt: bool | str = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: bool | None = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        help: str | None = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        # Rich settings
        rich_help_panel: str | None = None,
    ):
        if help:
            help = inspect.cleandoc(help)

        super().__init__(param_decls, type=type, multiple=multiple)

        if prompt is True:
            if self.name is None:
                raise TypeError("'name' is required with 'prompt=True'.")

            prompt_text: str | None = self.name.replace("_", " ").capitalize()
        elif prompt is False:
            prompt_text = None
        else:
            prompt_text = prompt

        self.prompt = prompt_text
        self.confirmation_prompt = confirmation_prompt
        self.prompt_required = prompt_required
        self.hide_input = hide_input
        self.hidden = hidden

        # TODO: remove?
        self._flag_needs_value = self.prompt is not None and not self.prompt_required

        if is_flag and type is None:
            self.type: _click.ParamType = _click.BoolParamType()

        self.is_flag: bool = bool(is_flag)
        self.is_bool_flag: bool = bool(
            is_flag and isinstance(self.type, _click.BoolParamType)
        )

        # Set boolean flag default to False if unset and not required.
        if self.is_bool_flag:
            if self.default is _click.UNSET and not self.required:
                self.default = False

        # Counting. TODO: test or remove? Not currently in coverage.
        self.count = count
        if count:
            if type is None:
                self.type = _click.IntRange(min=0)
            if self.default is _click.UNSET:
                self.default = 0

        self.allow_from_autoenv = allow_from_autoenv
        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar

        _typer_param_setup_autocompletion_compat(self, autocompletion=autocompletion)
        self.rich_help_panel = rich_help_panel

    def get_error_hint(self, ctx: Context) -> str:
        result = super().get_error_hint(ctx)
        if self.show_envvar and self.envvar is not None:
            result += f" (env var: '{self.envvar}')"
        return result

    def _parse_decls(
        self, decls: Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        opts = []
        secondary_opts = []
        name = None
        possible_names = []

        for decl in decls:
            if decl.isidentifier():
                if name is not None:
                    raise TypeError(f"Name '{name}' defined twice")
                name = decl
            else:
                split_char = ";" if decl[:1] == "/" else "/"
                if split_char in decl:
                    first, second = decl.split(split_char, 1)
                    first = first.rstrip()
                    if first:
                        possible_names.append(_split_opt(first))
                        opts.append(first)
                    second = second.lstrip()
                    if second:
                        secondary_opts.append(second.lstrip())
                    if first == second:
                        raise ValueError(
                            f"Boolean option {decl!r} cannot use the"
                            " same flag for true/false."
                        )
                else:
                    possible_names.append(_split_opt(decl))
                    opts.append(decl)

        if name is None and possible_names:
            possible_names.sort(key=lambda x: -len(x[0]))  # group long options first
            name = possible_names[0][1].replace("-", "_").lower()
            if not name.isidentifier():
                name = None

        return name, opts, secondary_opts

    def add_to_parser(self, parser: _click._OptionParser, ctx: Context) -> None:
        if self.multiple:
            action = "append"
        elif self.count:
            action = "count"
        else:
            action = "store"

        if self.is_flag:
            action = f"{action}_const"

            if self.is_bool_flag and self.secondary_opts:
                parser.add_option(
                    obj=self, opts=self.opts, dest=self.name, action=action, const=True
                )
                parser.add_option(
                    obj=self,
                    opts=self.secondary_opts,
                    dest=self.name,
                    action=action,
                    const=False,
                )
            else:
                parser.add_option(
                    obj=self,
                    opts=self.opts,
                    dest=self.name,
                    action=action,
                    # const=self.flag_value,
                )
        else:
            parser.add_option(
                obj=self,
                opts=self.opts,
                dest=self.name,
                action=action,
                nargs=self.nargs,
            )

    def get_help_extra(self, ctx: Context) -> _click.OptionHelpExtra:
        extra: _click.OptionHelpExtra = {}

        # TODO: no coverage. Test or remove?
        if self.show_envvar:
            envvar = self.envvar

            if envvar is None:
                if (
                    self.allow_from_autoenv
                    and ctx.auto_envvar_prefix is not None
                    and self.name is not None
                ):
                    envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"

            if envvar is not None:
                if isinstance(envvar, str):
                    extra["envvars"] = (envvar,)
                else:
                    extra["envvars"] = tuple(str(d) for d in envvar)

        # Temporarily enable resilient parsing to avoid type casting
        # failing for the default. Might be possible to extend this to
        # help formatting in general.
        resilient = ctx.resilient_parsing
        ctx.resilient_parsing = True

        try:
            default_value = self.get_default(ctx, call=False)
        finally:
            ctx.resilient_parsing = resilient

        show_default = False
        show_default_is_str = False

        # TODO: no coverage. Test or remove?
        if self.show_default is not None:
            if isinstance(self.show_default, str):
                show_default_is_str = show_default = True
            else:
                show_default = self.show_default
        elif ctx.show_default is not None:
            show_default = ctx.show_default

        if show_default_is_str or (
            show_default and (default_value not in (None, _click.UNSET))
        ):
            if show_default_is_str:
                default_string = f"({self.show_default})"
            elif isinstance(default_value, (list, tuple)):
                default_string = ", ".join(str(d) for d in default_value)
            elif isinstance(default_value, Enum):
                default_string = default_value.name
            elif inspect.isfunction(default_value):
                default_string = _("(dynamic)")
            elif self.is_bool_flag and self.secondary_opts:
                # For boolean flags that have distinct True/False opts,
                # use the opt without prefix instead of the value.
                default_string = _split_opt(
                    (self.opts if default_value else self.secondary_opts)[0]
                )[1]
            elif self.is_bool_flag and not self.secondary_opts and not default_value:
                default_string = ""
            elif default_value == "":
                default_string = '""'
            else:
                default_string = str(default_value)

            if default_string:
                extra["default"] = default_string

        # TODO: no coverage. Test or remove?
        if (
            isinstance(self.type, _click._NumberRangeBase)
            # skip count with default range type
            and not (self.count and self.type.min == 0 and self.type.max is None)
        ):
            range_str = self.type._describe_range()

            if range_str:
                extra["range"] = range_str

        if self.required:
            extra["required"] = "required"

        return extra

    def prompt_for_value(self, ctx: Context) -> Any:
        """This is an alternative flow that can be activated in the full
        value processing if a value does not exist.  It will prompt the
        user until a valid value exists and then returns the processed
        value as result.
        """
        assert self.prompt is not None

        # Calculate the default before prompting anything to lock in the value before
        # attempting any user interaction.
        default = self.get_default(ctx)

        # A boolean flag can use a simplified [y/n] confirmation prompt.
        if self.is_bool_flag:
            # If we have no boolean default, we force the user to explicitly provide
            # one.
            if default in (_click.UNSET, None):
                default = None
            # Nothing prevent you to declare an option that is simultaneously:
            # 1) auto-detected as a boolean flag,
            # 2) allowed to prompt, and
            # 3) still declare a non-boolean default.
            # This forced casting into a boolean is necessary to align any non-boolean
            # default to the prompt, which is going to be a [y/n]-style confirmation
            # because the option is still a boolean flag. That way, instead of [y/n],
            # we get [Y/n] or [y/N] depending on the truthy value of the default.
            # Refs: https://github.com/pallets/click/pull/3030#discussion_r2289180249
            else:
                default = bool(default)
            return _click.confirm(self.prompt, default)

        # If show_default is set to True/False, provide this to `prompt` as well. For
        # non-bool values of `show_default`, we use `prompt`'s default behavior
        prompt_kwargs: Any = {}
        if isinstance(self.show_default, bool):
            prompt_kwargs["show_default"] = self.show_default

        return _click.prompt(
            self.prompt,
            # Use ``None`` to inform the prompt() function to reiterate until a valid
            # value is provided by the user if we have no default.
            default=None if default is _click.UNSET else default,
            type=self.type,
            hide_input=self.hide_input,
            show_choices=self.show_choices,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_value(ctx, x),
            **prompt_kwargs,
        )

    def value_from_envvar(self, ctx: Context) -> Any:
        rv = self.resolve_envvar_value(ctx)

        # Absent environment variable or an empty string is interpreted as unset.
        if rv is None:
            return None

    def resolve_envvar_value(self, ctx: Context) -> str | None:
        rv = super().resolve_envvar_value(ctx)

        if rv is not None:
            return rv

        if (
            self.allow_from_autoenv
            and ctx.auto_envvar_prefix is not None
            and self.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"
            rv = os.environ.get(envvar)

            if rv:
                return rv

        return None

    def consume_value(
        self, ctx: Context, opts: Mapping[str, Parameter]
    ) -> tuple[Any, _click.ParameterSource]:
        """For :class:`Option`, the value can be collected from an interactive prompt
        if the option is a flag that needs a value (and the :attr:`prompt` property is
        set).

        Additionally, this method handles flag option that are activated without a
        value, in which case the :attr:`flag_value` is returned.
        """
        value, source = super().consume_value(ctx, opts)

        # TODO: evaluate this code. Needed for Typer?

        # Re-interpret a multiple option which has been sent as-is by the parser.
        # Here we replace each occurrence of value-less flags (marked by the
        # FLAG_NEEDS_VALUE sentinel) with the flag_value.
        if (
            self.multiple
            and value is not _click.UNSET
            and source
            not in (_click.ParameterSource.DEFAULT, _click.ParameterSource.DEFAULT_MAP)
            and any(v is _click.FLAG_NEEDS_VALUE for v in value)
        ):
            value = list(value)
            source = _click.ParameterSource.COMMANDLINE

        # The value wasn't set, or used the param's default, prompt for one to the user
        # if prompting is enabled.
        elif (
            (
                value is _click.UNSET
                or source
                in (_click.ParameterSource.DEFAULT, _click.ParameterSource.DEFAULT_MAP)
            )
            and self.prompt is not None
            and (self.required or self.prompt_required)
            and not ctx.resilient_parsing
        ):
            value = self.prompt_for_value(ctx)
            source = _click.ParameterSource.PROMPT

        return value, source

    def process_value(self, ctx: Context, value: Any) -> Any:
        # process_value has to be overridden on Options in order to capture
        # `value == UNSET` cases before `type_cast_value()` gets called.
        #
        # Refs:
        # https://github.com/pallets/click/issues/3069
        if (
            self.is_flag
            and not self.required
            and self.is_bool_flag
            and value is _click.UNSET
        ):
            value = False

            if self.callback is not None:
                value = self.callback(ctx, self, value)

            return value

        # in the normal case, rely on Parameter.process_value
        return super().process_value(ctx, value)

    def _get_default_string(
        self,
        *,
        ctx: Context,
        show_default_is_str: bool,
        default_value: list[Any] | tuple[Any, ...] | str | Callable[..., Any] | Any,
    ) -> str:
        return _get_default_string(
            self,
            ctx=ctx,
            show_default_is_str=show_default_is_str,
            default_value=default_value,
        )

    def _extract_default_help_str(
        self, *, ctx: Context
    ) -> Any | Callable[[], Any] | None:
        return _extract_default_help_str(self, ctx=ctx)

    def make_metavar(self, ctx: Context | None = None) -> str:
        return super().make_metavar(ctx=ctx)  # type: ignore[arg-type]

    def get_help_record(self, ctx: Context) -> tuple[str, str] | None:
        # Duplicate all of Click's logic only to modify a single line, to allow boolean
        # flags with only names for False values as it's currently supported by Typer
        # Ref: https://typer.tiangolo.com/tutorial/parameter-types/bool/#only-names-for-false
        if self.hidden:
            return None

        any_prefix_is_slash = False

        def _write_opts(opts: Sequence[str]) -> str:
            nonlocal any_prefix_is_slash

            rv, any_slashes = _click.formatting.join_options(opts)

            if any_slashes:
                any_prefix_is_slash = True

            if not self.is_flag and not self.count:
                rv += f" {self.make_metavar(ctx=ctx)}"

            return rv

        rv = [_write_opts(self.opts)]

        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ""
        extra = []

        if self.show_envvar:
            envvar = self.envvar

            if envvar is None:
                if (
                    self.allow_from_autoenv
                    and ctx.auto_envvar_prefix is not None
                    and self.name is not None
                ):
                    envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"

            if envvar is not None:
                var_str = (
                    envvar
                    if isinstance(envvar, str)
                    else ", ".join(str(d) for d in envvar)
                )
                extra.append(_("env var: {var}").format(var=var_str))

        # Typer override:
        # Extracted to _extract_default() to allow re-using it in rich_utils
        default_value = self._extract_default_help_str(ctx=ctx)
        # Typer override end

        show_default_is_str = isinstance(self.show_default, str)

        if show_default_is_str or (
            default_value is not None and (self.show_default or ctx.show_default)
        ):
            # Typer override:
            # Extracted to _get_default_string() to allow re-using it in rich_utils
            default_string = self._get_default_string(
                ctx=ctx,
                show_default_is_str=show_default_is_str,
                default_value=default_value,
            )
            # Typer override end
            if default_string:
                extra.append(_("default: {default}").format(default=default_string))

        if isinstance(self.type, _click.types._NumberRangeBase):
            range_str = self.type._describe_range()

            if range_str:
                extra.append(range_str)

        if self.required:
            extra.append(_("required"))

        if extra:
            extra_str = "; ".join(extra)
            extra_str = f"[{extra_str}]"
            rich_markup_mode = None
            if hasattr(ctx, "obj") and isinstance(ctx.obj, dict):
                rich_markup_mode = ctx.obj.get(MARKUP_MODE_KEY, None)
            if HAS_RICH and rich_markup_mode == "rich":
                # This is needed for when we want to export to HTML
                from . import rich_utils

                extra_str = rich_utils.escape_before_html_export(extra_str)

            help = f"{help}  {extra_str}" if help else f"{extra_str}"

        return ("; " if any_prefix_is_slash else " / ").join(rv), help

    def value_is_missing(self, value: Any) -> bool:
        return _value_is_missing(self, value)


def _value_is_missing(param: Parameter, value: Any) -> bool:
    if value is None:
        return True

    # Click 8.3 and beyond
    # if value is UNSET:
    #     return True

    if (param.nargs != 1 or param.multiple) and value == ():
        return True  # pragma: no cover

    return False


def _typer_format_options(
    self: TyperCommand, *, ctx: Context, formatter: _click.HelpFormatter
) -> None:
    args = []
    opts = []
    for param in self.get_params(ctx):
        rv = param.get_help_record(ctx)
        if rv is not None:
            if param.param_type_name == "argument":
                args.append(rv)
            elif param.param_type_name == "option":
                opts.append(rv)

    if args:
        with formatter.section(_("Arguments")):
            formatter.write_dl(args)
    if opts:
        with formatter.section(_("Options")):
            formatter.write_dl(opts)


def _typer_main_shell_completion(
    self: TyperCommand,
    *,
    ctx_args: MutableMapping[str, Any],
    prog_name: str,
    complete_var: str | None = None,
) -> None:
    if complete_var is None:
        complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

    instruction = os.environ.get(complete_var)

    if not instruction:
        return

    from .completion import shell_complete

    rv = shell_complete(self, ctx_args, prog_name, complete_var, instruction)
    sys.exit(rv)


def make_default_short_help(help: str, max_length: int = 45) -> str:
    """Returns a condensed version of help string."""
    # Consider only the first paragraph.
    paragraph_end = help.find("\n\n")

    if paragraph_end != -1:
        help = help[:paragraph_end]

    # Collapse newlines, tabs, and spaces.
    words = help.split()

    if not words:
        return ""

    # The first paragraph started with a "no rewrap" marker, ignore it.
    if words[0] == "\b":
        words = words[1:]

    total_length = 0
    last_index = len(words) - 1

    for i, word in enumerate(words):
        total_length += len(word) + (i > 0)

        if total_length > max_length:  # too long, truncate
            break

        if word[-1] == ".":  # sentence end, truncate without "..."
            return " ".join(words[: i + 1])

        if total_length == max_length and i != last_index:
            break  # not at sentence end, truncate with "..."
    else:
        return " ".join(words)  # no truncation needed

    # Account for the length of the suffix.
    total_length += len("...")

    # remove words until the length is short enough
    while i > 0:
        total_length -= len(words[i]) + (i > 0)

        if total_length <= max_length:
            break

        i -= 1

    return " ".join(words[:i]) + "..."


def iter_params_for_processing(
    invocation_order: Sequence[Parameter],
    declaration_order: Sequence[Parameter],
) -> list[Parameter]:
    """Returns all declared parameters in the order they should be processed.

    The declared parameters are re-shuffled depending on the order in which
    they were invoked, as well as the eagerness of each parameters.

    The invocation order takes precedence over the declaration order. I.e. the
    order in which the user provided them to the CLI is respected.

    This behavior and its effect on callback evaluation is detailed at:
    https://click.palletsprojects.com/en/stable/advanced/#callback-evaluation-order

    Original code from Click.
    """

    def sort_key(item: Parameter) -> tuple[bool, float]:
        try:
            idx: float = invocation_order.index(item)
        except ValueError:
            idx = float("inf")

        return not item.is_eager, idx

    return sorted(declaration_order, key=sort_key)


class TyperCommand:
    context_class: type[Context] = Context
    allow_extra_args = False
    allow_interspersed_args = True
    ignore_unknown_options = False
    _help_option: TyperOption | None = None

    def __init__(
        self,
        name: str | None,
        *,
        context_settings: dict[str, Any] | None = None,
        callback: Callable[..., Any] | None = None,
        params: list[Parameter] | None = None,
        help: str | None = None,
        epilog: str | None = None,
        short_help: str | None = None,
        options_metavar: str | None = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        # Rich settings
        rich_markup_mode: MarkupMode = DEFAULT_MARKUP_MODE,
        rich_help_panel: str | None = None,
    ) -> None:
        self.name = name
        self.context_settings: MutableMapping[str, Any] = context_settings or {}
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
        # Rich settings
        self.rich_markup_mode: MarkupMode = rich_markup_mode
        self.rich_help_panel = rich_help_panel

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def get_usage(self, ctx: Context) -> str:
        formatter = ctx.make_formatter()
        self.format_usage(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def get_params(self, ctx: Context) -> list[Parameter]:
        params = self.params
        help_option = self.get_help_option(ctx)

        if help_option is not None:
            params = [*params, help_option]

        return params

    def format_usage(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        formatter.write_usage(ctx.command_path, " ".join(pieces))

    def collect_usage_pieces(self, ctx: Context) -> list[str]:
        rv = [self.options_metavar] if self.options_metavar else []

        for param in self.get_params(ctx):
            rv.extend(param.get_usage_pieces(ctx))

        return rv

    def get_help_option_names(self, ctx: Context) -> list[str]:
        all_names = set(ctx.help_option_names)
        for param in self.params:
            all_names.difference_update(param.opts)
            all_names.difference_update(param.secondary_opts)
        return list(all_names)

    def get_help_option(self, ctx: Context) -> TyperOption | None:
        help_option_names = self.get_help_option_names(ctx)

        if not help_option_names or not self.add_help_option:
            return None

        # Cache the help option object in private _help_option attribute to
        # avoid creating it multiple times. Not doing this will break the
        # callback ordering by iter_params_for_processing(), which relies on
        # object comparison.
        if self._help_option is None:

            def show_help(ctx: Context, param: Parameter, value: bool) -> None:
                """Callback that print the help page on ``<stdout>`` and exits."""
                if value and not ctx.resilient_parsing:
                    echo(ctx.get_help(), color=ctx.color)
                    ctx.exit()

            self._help_option = TyperOption(param_decls=help_option_names, is_flag=True, expose_value=False, is_eager=True, help="Show this message and exit.", callback=show_help)

        return self._help_option

    def get_help(self, ctx: Context) -> str:
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

        # TODO: add test or remove code
        if self.deprecated:
            deprecated_message = (
                f"(DEPRECATED: {self.deprecated})"
                if isinstance(self.deprecated, str)
                else "(DEPRECATED)"
            )
            text = _("{text} {deprecated_message}").format(
                text=text, deprecated_message=deprecated_message
            )

        return text.strip()

    def _format_help_click(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        """Writes the help text to the formatter if it exists."""
        if self.help is not None:
            # truncate the help text to the first form feed
            text = inspect.cleandoc(self.help).partition("\f")[0]
        else:
            text = ""

        # TODO: add test or remove code
        if self.deprecated:
            deprecated_message = (
                f"(DEPRECATED: {self.deprecated})"
                if isinstance(self.deprecated, str)
                else "(DEPRECATED)"
            )
            text = _("{text} {deprecated_message}").format(
                text=text, deprecated_message=deprecated_message
            )

        if text:
            formatter.write_paragraph()

            with formatter.indentation():
                formatter.write_text(text)

    def make_parser(self, ctx: Context) -> _click._OptionParser:
        """Creates the underlying option parser for this command."""
        parser = _click._OptionParser(ctx)
        for param in self.get_params(ctx):
            param.add_to_parser(parser, ctx)
        return parser

    def format_options(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        _typer_format_options(self, ctx=ctx, formatter=formatter)

    def format_epilog(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        # TODO: add test for self.epilog=True, or remove code
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
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value

        ctx = self.context_class(self, info_name=info_name, parent=parent, **extra)

        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)
        return ctx

    def _main_shell_completion(
        self,
        ctx_args: MutableMapping[str, Any],
        prog_name: str,
        complete_var: str | None = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )

    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        return _main(
            self,
            args=args,
            prog_name=prog_name,
            complete_var=complete_var,
            standalone_mode=standalone_mode,
            windows_expand_args=windows_expand_args,
            rich_markup_mode=self.rich_markup_mode,
            **extra,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.main(*args, **kwargs)

    def format_help(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        if not HAS_RICH or self.rich_markup_mode is None:
            if not hasattr(ctx, "obj") or ctx.obj is None:
                ctx.ensure_object(dict)
            if isinstance(ctx.obj, dict):
                ctx.obj[MARKUP_MODE_KEY] = self.rich_markup_mode
            return self._format_help_click(ctx, formatter)
        from . import rich_utils

        return rich_utils.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
        )

    def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            raise _click.NoArgsIsHelpError(ctx)

        parser = self.make_parser(ctx)
        opts, args, param_order = parser.parse_args(args=args)

        for param in iter_params_for_processing(param_order, self.get_params(ctx)):
            _, args = param.handle_parse_result(ctx, opts, args)

        # We now have all parameters' values into `ctx.params`, but the data may contain
        # the `UNSET` sentinel.
        # Convert `UNSET` to `None` to ensure that the user doesn't see `UNSET`.
        #
        # Waiting until after the initial parse to convert allows us to treat `UNSET`
        # more like a missing value when multiple params use the same name.
        # Refs:
        # https://github.com/pallets/click/issues/3071
        # https://github.com/pallets/click/pull/3079
        for name, value in ctx.params.items():
            if value is _click.UNSET:
                ctx.params[name] = None

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
            message = _(
                "DeprecationWarning: The command {name!r} is deprecated.{extra_message}"
            ).format(name=self.name, extra_message=extra_message)
            _click.echo(_click.style(message, fg="red"), err=True)

        if self.callback is not None:
            return ctx.invoke(self.callback, **ctx.params)

    def shell_complete(
        self, ctx: Context, incomplete: str
    ) -> list[_click.CompletionItem]:
        results: list[_click.CompletionItem] = []

        if incomplete and not incomplete[0].isalnum():
            for param in self.get_params(ctx):
                if (
                    not isinstance(param, TyperOption)
                    or isinstance(param, TyperArgument) and param.hidden
                    or (
                        not param.multiple
                        and ctx.get_parameter_source(param.name)  # type: ignore
                        is _click.ParameterSource.COMMANDLINE
                    )
                ):
                    continue

                results.extend(
                    _click.CompletionItem(name, help=param.help)
                    for name in [*param.opts, *param.secondary_opts]
                    if name.startswith(incomplete)
                )

        return results


def _complete_visible_commands(
    ctx: Context, incomplete: str
) -> Iterator[tuple[str, TyperCommand]]:
    """List all the subcommands of a group that start with the
    incomplete value and aren't hidden.

    :param ctx: Invocation context for the group.
    :param incomplete: Value being completed. May be empty.
    """
    multi = cast(TyperGroup, ctx.command)

    for name in multi.list_commands(ctx):
        if name.startswith(incomplete):
            command = multi.get_command(ctx, name)

            if command is not None and not command.hidden:
                yield name, command


class TyperGroup(TyperCommand):
    allow_extra_args = True
    allow_interspersed_args = False

    command_class: type[TyperCommand] | None = None

    group_class: type[TyperGroup] | type[type] | None = None

    def __init__(
        self,
        *,
        name: str | None = None,
        commands: dict[str, TyperCommand] | Sequence[TyperCommand] | None = None,
        # Rich settings
        rich_markup_mode: MarkupMode = DEFAULT_MARKUP_MODE,
        rich_help_panel: str | None = None,
        suggest_commands: bool = True,
        # Click settings
        invoke_without_command: bool = False,
        no_args_is_help: bool = False,
        subcommand_metavar: str | None = None,
        result_callback: Callable[..., Any] | None = None,
        **attrs: Any,
    ) -> None:
        super().__init__(name=name, **attrs)
        self.rich_markup_mode: MarkupMode = rich_markup_mode
        self.rich_help_panel = rich_help_panel
        self.suggest_commands = suggest_commands

        # copied from Click's init
        if commands is None:
            commands = {}
        elif isinstance(commands, Sequence):
            commands = {c.name: c for c in commands if c.name is not None}

        #: The registered subcommands by their exported names.
        self.commands: MutableMapping[str, TyperCommand] = commands

        self.no_args_is_help = no_args_is_help
        self.invoke_without_command = invoke_without_command

        if subcommand_metavar is None:
            subcommand_metavar = "COMMAND [ARGS]..."

        self.subcommand_metavar = subcommand_metavar
        # The result callback that is stored. This can be set or
        # overridden with the :func:`result_callback` decorator.
        self._result_callback = result_callback

    def add_command(self, cmd: TyperCommand, name: str | None = None) -> None:
        name = name or cmd.name
        if name is None:
            raise TypeError("Command has no name.")
        self.commands[name] = cmd

    def get_command(self, ctx: Context, cmd_name: str) -> TyperCommand | None:
        return self.commands.get(cmd_name)

    def collect_usage_pieces(self, ctx: Context) -> list[str]:
        rv = super().collect_usage_pieces(ctx)
        rv.append(self.subcommand_metavar)
        return rv

    def format_commands(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                assert cmd is not None
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section(_("Commands")):
                    formatter.write_dl(rows)

    def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            raise _click.NoArgsIsHelpError(ctx)

        rest = super().parse_args(ctx, args)

        if rest:
            ctx.args = rest

        return ctx.args

    def invoke(self, ctx: Context) -> Any:
        def _process_result(value: Any) -> Any:
            if self._result_callback is not None:
                value = ctx.invoke(self._result_callback, value, **ctx.params)
            return value

        if self.invoke_without_command:
            # No subcommand was invoked, so the result callback is
            # invoked with the group return value
            with ctx:
                rv = super().invoke(ctx)
                return _process_result(rv)
        ctx.fail(_("Missing command."))

        # Fetch args back out
        args = [*ctx.args]
        ctx.args = []

        # Make sure the context is entered so we do not clean up
        # resources until the result processor has worked.
        with ctx:
            cmd_name, cmd, args = self.resolve_command(ctx, args)
            assert cmd is not None
            ctx.invoked_subcommand = cmd_name
            super().invoke(ctx)
            sub_ctx = cmd.make_context(cmd_name, args, parent=ctx)
            with sub_ctx:
                return _process_result(sub_ctx.command.invoke(sub_ctx))

    def shell_complete(
        self, ctx: Context, incomplete: str
    ) -> list[_click.CompletionItem]:
        """Return a list of completions for the incomplete value. Looks
        at the names of options, subcommands, and chained
        multi-commands.

        :param ctx: Invocation context for this command.
        :param incomplete: Value being completed. May be empty.
        """

        results = [
            _click.CompletionItem(name, help=command.get_short_help_str())
            for name, command in _complete_visible_commands(ctx, incomplete)
        ]
        results.extend(super().shell_complete(ctx, incomplete))
        return results

    def format_options(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        _typer_format_options(self, ctx=ctx, formatter=formatter)
        self.format_commands(ctx, formatter)

    def _main_shell_completion(
        self,
        ctx_args: MutableMapping[str, Any],
        prog_name: str,
        complete_var: str | None = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )

    def click_resolve_command(self, ctx: Context, args: list[str]) -> tuple[str | None, TyperCommand | None, list[str]]:
        cmd_name = make_str(args[0])
        original_cmd_name = cmd_name

        # Get the command
        cmd = self.get_command(ctx, cmd_name)

        # If we can't find the command but there is a normalization
        # function available, we try with that one.
        if cmd is None and ctx.token_normalize_func is not None:
            cmd_name = ctx.token_normalize_func(cmd_name)
            cmd = self.get_command(ctx, cmd_name)

        # If we don't find the command we want to show an error message
        # to the user that it was not provided.  However, there is
        # something else we should do: if the first argument looks like
        # an option we want to kick off parsing again for arguments to
        # resolve things like --help which now should go to the main
        # place.
        if cmd is None and not ctx.resilient_parsing:
            if _split_opt(cmd_name)[0]:
                self.parse_args(ctx, args)
            ctx.fail(_("No such command {name!r}.").format(name=original_cmd_name))
        return cmd_name if cmd else None, cmd, args[1:]

    def resolve_command(
        self, ctx: Context, args: list[str]
    ) -> tuple[str | None, TyperCommand | None, list[str]]:
        try:
            return self.click_resolve_command(ctx, args)
        except _click.UsageError as e:
            if self.suggest_commands:
                available_commands = list(self.commands.keys())
                if available_commands and args:
                    typo = args[0]
                    matches = get_close_matches(typo, available_commands)
                    if matches:
                        suggestions = ", ".join(f"{m!r}" for m in matches)
                        message = e.message.rstrip(".")
                        e.message = f"{message}. Did you mean {suggestions}?"
            raise

    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        return _main(
            self,
            args=args,
            prog_name=prog_name,
            complete_var=complete_var,
            standalone_mode=standalone_mode,
            windows_expand_args=windows_expand_args,
            rich_markup_mode=self.rich_markup_mode,
            **extra,
        )

    def format_help(self, ctx: Context, formatter: _click.HelpFormatter) -> None:
        if not HAS_RICH or self.rich_markup_mode is None:
            return super().format_help(ctx, formatter)
        from . import rich_utils

        return rich_utils.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
        )

    def list_commands(self, ctx: Context) -> list[str]:
        """Returns a list of subcommand names.
        In Typer, we wish to maintain the original order of creation (cf Issue #933)"""
        return [n for n, c in self.commands.items()]
