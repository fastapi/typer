import inspect
from typing import Any, Callable, List, Optional, Tuple, Union

import click.core


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
            autocompletion=autocompletion,
        )

    def get_help_record(self, ctx: click.Context) -> Optional[Tuple[str, str]]:  # type: ignore
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
        if self.default is not None and (self.show_default or ctx.show_default):  # type: ignore
            if isinstance(self.show_default, str):
                default_string = f"({self.show_default})"
            elif isinstance(self.default, (list, tuple)):
                default_string = ", ".join(str(d) for d in self.default)
            elif inspect.isfunction(self.default):
                default_string = "(dynamic)"
            else:
                default_string = self.default
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
        var = self.name.upper()
        if not self.required:
            var = "[{}]".format(var)
        type_var = self.type.get_metavar(self)
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var


class TyperCommand(click.core.Command):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
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
            with formatter.section("Arguments"):
                formatter.write_dl(args)
        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)
