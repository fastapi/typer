from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

from .core import Command, Context, Parameter
from .utils import echo

if TYPE_CHECKING:
    from ..core import TyperGroup, TyperOption

    GrpType = TypeVar("GrpType", bound=TyperGroup)


P = ParamSpec("P")

R = TypeVar("R")
T = TypeVar("T")
_AnyCallable = Callable[..., Any]


CmdType = TypeVar("CmdType", bound=Command)


def option(
    *param_decls: str, cls: type["TyperOption"] | None = None, **attrs: Any
) -> Callable[[Command], Command]:
    """Attaches an option to the command.  All positional arguments are
    passed as parameter declarations to `Option`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an `Option` instance manually
    and attaching it to the `Command.params` list.

    For the default option class, refer to `Option` and
    `Parameter` for descriptions of parameters.
    """
    if cls is None:
        # avoid circular imports
        from ..core import TyperOption

        cls = TyperOption

    def decorator(f: Command) -> Command:
        param = cls(param_decls=list(param_decls), **attrs)
        f.params.append(param)
        return f

    return decorator


def help_option(*param_decls: str, **kwargs: Any) -> Callable[[Command], Command]:
    """Pre-configured ``--help`` option which immediately prints the help page
    and exits the program.
    """

    def show_help(ctx: Context, param: Parameter, value: bool) -> None:
        """Callback that print the help page on ``<stdout>`` and exits."""
        if value and not ctx.resilient_parsing:
            echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

    if not param_decls:
        param_decls = ("--help",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", "Show this message and exit.")
    kwargs.setdefault("callback", show_help)
    kwargs.setdefault("required", False)

    return option(*param_decls, **kwargs)
