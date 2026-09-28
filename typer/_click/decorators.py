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
    param_decls: list[str], cls: type["TyperOption"] | None = None, **attrs: Any
) -> Callable[[Command], Command]:
    """Attaches an option to the command."""
    if cls is None:
        # avoid circular imports
        from ..core import TyperOption

        cls = TyperOption

    def decorator(f: Command) -> Command:
        param = cls(param_decls=param_decls, **attrs)
        f.params.append(param)
        return f

    return decorator


def help_option(param_decls: list[str]) -> Callable[[Command], Command]:
    """Help option which prints the help page and exits the program."""

    def show_help(ctx: Context, param: Parameter, value: bool) -> None:
        """Callback that print the help page on ``<stdout>`` and exits."""
        if value and not ctx.resilient_parsing:
            echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

    assert len(param_decls) > 0, "At least one help option should be provided"

    return option(
        param_decls,
        is_flag=True,
        expose_value=False,
        is_eager=True,
        help="Show this message and exit.",
        callback=show_help,
        required=False,
    )
