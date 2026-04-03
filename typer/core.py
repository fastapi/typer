from __future__ import annotations

import errno
import inspect
import os
import sys
from collections.abc import Callable, Iterator, MutableMapping, Sequence
from difflib import get_close_matches
from enum import Enum
from gettext import gettext as _
from typing import (
    Any,
    TextIO,
    TypeVar,
    cast,
)

from . import Context, Option, _click
from ._typing import Literal
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
    self: _click.Parameter,
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
            ctx: Context, param: _click.core.Parameter, incomplete: str
        ) -> list[_click.shell_completion.CompletionItem]:
            out = []

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


class TyperArgument(_click.core.Argument):
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
            [Context, _click.Parameter, str],
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
        type_var = self.type.get_metavar(self, ctx=ctx)  # type: ignore[arg-type]
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var

    def value_is_missing(self, value: Any) -> bool:
        return _value_is_missing(self, value)


class TyperOption(_click.core.Option):
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
            [Context, _click.Parameter, str],
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
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            hide_input=hide_input,
            is_flag=is_flag,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
            prompt_required=prompt_required,
            shell_complete=shell_complete,
        )
        _typer_param_setup_autocompletion_compat(self, autocompletion=autocompletion)
        self.rich_help_panel = rich_help_panel

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


def _value_is_missing(param: _click.Parameter, value: Any) -> bool:
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
    self: _click.core.Command,
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
    invocation_order: Sequence[_click.Parameter],
    declaration_order: Sequence[_click.Parameter],
) -> list[_click.Parameter]:
    """Returns all declared parameters in the order they should be processed.

    The declared parameters are re-shuffled depending on the order in which
    they were invoked, as well as the eagerness of each parameters.

    The invocation order takes precedence over the declaration order. I.e. the
    order in which the user provided them to the CLI is respected.

    This behavior and its effect on callback evaluation is detailed at:
    https://click.palletsprojects.com/en/stable/advanced/#callback-evaluation-order

    Original code from Click.
    """

    def sort_key(item: _click.Parameter) -> tuple[bool, float]:
        try:
            idx: float = invocation_order.index(item)
        except ValueError:
            idx = float("inf")

        return not item.is_eager, idx

    return sorted(declaration_order, key=sort_key)


class TyperCommand(_click.core.Command):
    context_class: type[Context] = Context

    #: the default for the :attr:`Context.allow_extra_args` flag.
    allow_extra_args = False

    #: the default for the :attr:`Context.allow_interspersed_args` flag.
    allow_interspersed_args = True

    #: the default for the :attr:`Context.ignore_unknown_options` flag.
    ignore_unknown_options = False

    def __init__(
        self,
        name: str | None,
        *,
        context_settings: dict[str, Any] | None = None,
        callback: Callable[..., Any] | None = None,
        params: list[_click.Parameter] | None = None,
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
        self.params: list[_click.Parameter] = params or []
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

    def get_params(self, ctx: Context) -> list[_click.Parameter]:
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

    def get_help_option(self, ctx: Context) -> Option | None:
        help_option_names = self.get_help_option_names(ctx)

        if not help_option_names or not self.add_help_option:
            return None

        # Click functionality:
        # Cache the help option object in private _help_option attribute to
        # avoid creating it multiple times. Not doing this will break the
        # callback ordering by iter_params_for_processing(), which relies on
        # object comparison.
        if self._help_option is None:
            # Avoid circular import.
            from _click.decorators import help_option

            # Apply help_option decorator and pop resulting option
            help_option(*help_option_names)(self)
            self._help_option = self.params.pop()  # type: ignore[assignment]

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
                    not isinstance(param, Option)
                    or param.hidden
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

        while ctx.parent is not None:
            ctx = ctx.parent

            if isinstance(ctx.command, TyperGroup) and ctx.command.chain:
                results.extend(
                    _click.CompletionItem(name, help=command.get_short_help_str())
                    for name, command in _complete_visible_commands(ctx, incomplete)
                    if name not in ctx._protected_args
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
            ctx._protected_args, ctx.args = rest[:1], rest[1:]

        return ctx.args

    def invoke(self, ctx: Context) -> Any:
        def _process_result(value: Any) -> Any:
            if self._result_callback is not None:
                value = ctx.invoke(self._result_callback, value, **ctx.params)
            return value

        if not ctx._protected_args:
            if self.invoke_without_command:
                # No subcommand was invoked, so the result callback is
                # invoked with the group return value for regular
                # groups, or an empty list for chained groups.
                with ctx:
                    rv = super().invoke(ctx)
                    return _process_result([] if self.chain else rv)
            ctx.fail(_("Missing command."))

        # Fetch args back out
        args = [*ctx._protected_args, *ctx.args]
        ctx.args = []
        ctx._protected_args = []

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

    def resolve_command(
        self, ctx: Context, args: list[str]
    ) -> tuple[str | None, TyperCommand | None, list[str]]:
        try:
            return super().resolve_command(ctx, args)
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
