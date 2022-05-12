import inspect
import os
import sys
from gettext import gettext as _
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import click
import click.core
import click.formatting
import click.parser
import click.types

from .utils import _get_click_major

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion


# TODO: when deprecating Click 7, remove this
def _typer_param_shell_complete(
    self: click.core.Parameter, ctx: click.Context, incomplete: str
) -> List["click.shell_completion.CompletionItem"]:
    if self._custom_shell_complete is not None:
        results = self._custom_shell_complete(ctx, self, incomplete)

        if results and isinstance(results[0], str):
            from click.shell_completion import CompletionItem

            results = [CompletionItem(c) for c in results]

        return cast(List["click.shell_completion.CompletionItem"], results)

    return self.type.shell_complete(ctx, self, incomplete)


def _typer_param_setup_autocompletion_compat(
    self: click.Parameter,
    *,
    autocompletion: Optional[
        Callable[[click.Context, List[str], str], List[Union[Tuple[str, str], str]]]
    ] = None,
) -> None:
    if autocompletion is not None and self._custom_shell_complete is None:
        import warnings

        warnings.warn(
            "'autocompletion' is renamed to 'shell_complete'. The old name is"
            " deprecated and will be removed in Click 8.1. See the docs about"
            " 'Parameter' for information about new behavior.",
            DeprecationWarning,
            stacklevel=2,
        )

        def compat_autocompletion(
            ctx: click.Context, param: click.core.Parameter, incomplete: str
        ) -> List["click.shell_completion.CompletionItem"]:
            from click.shell_completion import CompletionItem

            out = []

            for c in autocompletion(ctx, [], incomplete):  # type: ignore
                if isinstance(c, tuple):
                    c = CompletionItem(c[0], help=c[1])
                elif isinstance(c, str):
                    c = CompletionItem(c)

                if c.value.startswith(incomplete):
                    out.append(c)

            return out

        self._custom_shell_complete = compat_autocompletion


class TyperArgument(click.core.Argument):
    def __init__(
        self,
        *,
        # Parameter
        param_decls: List[str],
        type: Optional[Any] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        # TyperArgument
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
    ):
        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar
        self.hidden = hidden
        kwargs: Dict[str, Any] = {
            "param_decls": param_decls,
            "type": type,
            "required": required,
            "default": default,
            "callback": callback,
            "nargs": nargs,
            "metavar": metavar,
            "expose_value": expose_value,
            "is_eager": is_eager,
            "envvar": envvar,
        }
        if _get_click_major() > 7:
            kwargs["shell_complete"] = shell_complete
        else:
            kwargs["autocompletion"] = autocompletion
        super().__init__(**kwargs)
        if _get_click_major() > 7:
            _typer_param_setup_autocompletion_compat(
                self, autocompletion=autocompletion
            )

    def get_help_record(self, ctx: click.Context) -> Optional[Tuple[str, str]]:
        # Modified version of click.core.Option.get_help_record()
        # to support Arguments
        if self.hidden:
            return None
        name = self.make_metavar()
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
        if self.default is not None and (self.show_default or ctx.show_default):
            if isinstance(self.show_default, str):
                default_string = f"({self.show_default})"
            elif isinstance(self.default, (list, tuple)):
                default_string = ", ".join(str(d) for d in self.default)
            elif inspect.isfunction(self.default):
                default_string = "(dynamic)"
            else:
                default_string = str(self.default)
            extra.append(f"default: {default_string}")
        if self.required:
            extra.append("required")
        if extra:
            extra_str = ";".join(extra)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"
        return name, help

    def make_metavar(self) -> str:
        # Modified version of click.core.Argument.make_metavar()
        # to include Argument name
        if self.metavar is not None:
            return self.metavar
        var = (self.name or "").upper()
        if not self.required:
            var = "[{}]".format(var)
        type_var = self.type.get_metavar(self)
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var

    def shell_complete(
        self, ctx: click.Context, incomplete: str
    ) -> List["click.shell_completion.CompletionItem"]:
        return _typer_param_shell_complete(self, ctx=ctx, incomplete=incomplete)


class TyperOption(click.core.Option):
    def __init__(
        self,
        *,
        # Parameter
        param_decls: List[str],
        type: Optional[Union[click.types.ParamType, Any]] = None,
        required: Optional[bool] = None,
        default: Optional[Any] = None,
        callback: Optional[Callable[..., Any]] = None,
        nargs: Optional[int] = None,
        metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[List["click.shell_completion.CompletionItem"], List[str]],
            ]
        ] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        # Option
        show_default: Union[bool, str] = False,
        prompt: Union[bool, str] = False,
        confirmation_prompt: Union[bool, str] = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
    ):
        # TODO: when deprecating Click 7, remove custom kwargs with prompt_required
        # and call super().__init__() directly
        kwargs: Dict[str, Any] = {
            "param_decls": param_decls,
            "type": type,
            "required": required,
            "default": default,
            "callback": callback,
            "nargs": nargs,
            "metavar": metavar,
            "expose_value": expose_value,
            "is_eager": is_eager,
            "envvar": envvar,
            "show_default": show_default,
            "prompt": prompt,
            "confirmation_prompt": confirmation_prompt,
            "hide_input": hide_input,
            "is_flag": is_flag,
            "flag_value": flag_value,
            "multiple": multiple,
            "count": count,
            "allow_from_autoenv": allow_from_autoenv,
            "help": help,
            "hidden": hidden,
            "show_choices": show_choices,
            "show_envvar": show_envvar,
        }
        if _get_click_major() > 7:
            kwargs["prompt_required"] = prompt_required
            kwargs["shell_complete"] = shell_complete
        else:
            kwargs["autocompletion"] = autocompletion
        super().__init__(**kwargs)
        if _get_click_major() > 7:
            _typer_param_setup_autocompletion_compat(
                self, autocompletion=autocompletion
            )

    def get_help_record(self, ctx: click.Context) -> Optional[Tuple[str, str]]:
        # Click 7.x was not breaking this use case, so in that case, re-use its logic
        if _get_click_major() < 8:
            return super().get_help_record(ctx)
        # Duplicate all of Click's logic only to modify a single line, to allow boolean
        # flags with only names for False values as it's currently supported by Typer
        # Ref: https://typer.tiangolo.com/tutorial/parameter-types/bool/#only-names-for-false
        if self.hidden:
            return None

        any_prefix_is_slash = False

        def _write_opts(opts: Sequence[str]) -> str:
            nonlocal any_prefix_is_slash

            rv, any_slashes = click.formatting.join_options(opts)

            if any_slashes:
                any_prefix_is_slash = True

            if not self.is_flag and not self.count:
                rv += f" {self.make_metavar()}"

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

        # Temporarily enable resilient parsing to avoid type casting
        # failing for the default. Might be possible to extend this to
        # help formatting in general.
        resilient = ctx.resilient_parsing
        ctx.resilient_parsing = True

        try:
            default_value = self.get_default(ctx, call=False)
        finally:
            ctx.resilient_parsing = resilient

        show_default_is_str = isinstance(self.show_default, str)

        if show_default_is_str or (
            default_value is not None and (self.show_default or ctx.show_default)
        ):
            if show_default_is_str:
                default_string = f"({self.show_default})"
            elif isinstance(default_value, (list, tuple)):
                default_string = ", ".join(str(d) for d in default_value)
            elif callable(default_value):
                default_string = _("(dynamic)")
            elif self.is_bool_flag and self.secondary_opts:
                # For boolean flags that have distinct True/False opts,
                # use the opt without prefix instead of the value.
                # Typer override, original commented
                # default_string = click.parser.split_opt(
                #     (self.opts if self.default else self.secondary_opts)[0]
                # )[1]
                if self.default:
                    if self.opts:
                        default_string = click.parser.split_opt(self.opts[0])[1]
                    else:
                        default_string = str(default_value)
                else:
                    default_string = click.parser.split_opt(self.secondary_opts[0])[1]
                # Typer override end
            elif self.is_bool_flag and not self.secondary_opts and not default_value:
                default_string = ""
            else:
                default_string = str(default_value)

            if default_string:
                extra.append(_("default: {default}").format(default=default_string))

        if isinstance(self.type, click.types._NumberRangeBase):
            range_str = self.type._describe_range()

            if range_str:
                extra.append(range_str)

        if self.required:
            extra.append(_("required"))

        if extra:
            extra_str = "; ".join(extra)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"

        return ("; " if any_prefix_is_slash else " / ").join(rv), help

    def shell_complete(
        self, ctx: click.Context, incomplete: str
    ) -> List["click.shell_completion.CompletionItem"]:
        return _typer_param_shell_complete(self, ctx=ctx, incomplete=incomplete)


def _typer_format_options(
    self: click.core.Command, *, ctx: click.Context, formatter: click.HelpFormatter
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

    # TODO: explore adding Click's gettext support, e.g.:
    # from gettext import gettext as _
    # with formatter.section(_("Options")):
    #     ...
    if args:
        with formatter.section("Arguments"):
            formatter.write_dl(args)
    if opts:
        with formatter.section("Options"):
            formatter.write_dl(opts)


def _typer_main_shell_completion(
    self: click.core.Command,
    *,
    ctx_args: Dict[str, Any],
    prog_name: str,
    complete_var: Optional[str] = None,
) -> None:
    if complete_var is None:
        complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

    instruction = os.environ.get(complete_var)

    if not instruction:
        return

    from .completion import shell_complete

    rv = shell_complete(self, ctx_args, prog_name, complete_var, instruction)
    sys.exit(rv)


class TyperCommand(click.core.Command):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        _typer_format_options(self, ctx=ctx, formatter=formatter)

    def _main_shell_completion(
        self,
        ctx_args: Dict[str, Any],
        prog_name: str,
        complete_var: Optional[str] = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )


class TyperGroup(click.core.Group):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        _typer_format_options(self, ctx=ctx, formatter=formatter)
        self.format_commands(ctx, formatter)

    def _main_shell_completion(
        self,
        ctx_args: Dict[str, Any],
        prog_name: str,
        complete_var: Optional[str] = None,
    ) -> None:
        _typer_main_shell_completion(
            self, ctx_args=ctx_args, prog_name=prog_name, complete_var=complete_var
        )
