import sys
from gettext import gettext as _
from typing import Any

from . import _click
from .core import DEFAULT_MARKUP_MODE, HAS_RICH, TyperCommand, TyperGroup
from .models import ParamMeta
from .params import Option
from .utils import get_params_from_function

SUBCMD_INDENT = "  "
SUBCOMMAND_TITLE = _("Sub-Commands")


def _subcommand_items(
    command: TyperCommand | TyperGroup | Any, indent_level: int
) -> list[tuple[str, str]]:
    if not isinstance(command, (TyperGroup, TyperCommand)):
        return []  # pragma: no cover

    items = []
    subcommands = command.commands if isinstance(command, TyperGroup) else {}

    # get info for this command
    indent = SUBCMD_INDENT * indent_level
    note = "*" if not subcommands else ""
    name = indent + (command.name or "unknown") + note
    help = command.short_help or command.help or ""
    items.append((name, help))

    # recursively call for sub-commands with larger indent
    for subcommand in subcommands.values():
        if subcommand.hidden:
            continue
        items.extend(_subcommand_items(subcommand, indent_level + 1))

    return items


def show_command_tree(
    ctx: _click.Context,
    param: _click.Parameter,
    value: Any,
) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma: no cover

    command = ctx.command
    if not isinstance(command, TyperGroup):
        return value  # pragma: no cover
    items = []
    for subcommand in command.commands.values():
        if subcommand.hidden:
            continue
        items.extend(_subcommand_items(subcommand, 0))

    if items:
        markup_mode = DEFAULT_MARKUP_MODE
        if not HAS_RICH or markup_mode is None:  # pragma: no cover
            formatter = ctx.make_formatter()
            formatter.section(SUBCOMMAND_TITLE)
            formatter.write_dl(items)
            content = formatter.getvalue().rstrip("\n")
            _click.echo(content)
        else:
            from . import rich_utils

            rich_utils.rich_format_subcommands(ctx, items)

    sys.exit(0)


# Create a fake command function to extract parameters
def _show_command_tree_placeholder_function(
    show_command_tree: bool = Option(
        None,
        "--show-sub-commands",
        callback=show_command_tree,
        expose_value=False,
        help="Show sub-command tree",
    ),
) -> Any:
    pass  # pragma: no cover


def get_command_tree_param_meta() -> ParamMeta:
    parameters = get_params_from_function(_show_command_tree_placeholder_function)
    meta_values = list(parameters.values())  # currently only one value
    return meta_values[0]
