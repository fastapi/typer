import sys
from gettext import gettext as _
from typing import Any, Dict, List, Literal, Tuple

import click

from .models import ParamMeta
from .params import Option
from .utils import get_params_from_function

MarkupMode = Literal["markdown", "rich", None]

try:
    import rich

    from . import rich_utils

    DEFAULT_MARKUP_MODE: MarkupMode = "rich"

except ImportError:  # pragma: no cover
    rich = None  # type: ignore
    DEFAULT_MARKUP_MODE = None


SUBCMD_INDENT = "  "
SUBCOMMAND_TITLE = _("Sub-Commands")


def _commands_from_info(
    info: Dict[str, Any], indent_level: int
) -> List[Tuple[str, str]]:
    items = []
    subcommands = info.get("commands", {})

    # get info for this command
    indent = SUBCMD_INDENT * indent_level
    note = "*" if not subcommands else ""
    name = indent + info.get("name", "unknown") + note
    help = info.get("short_help") or info.get("help") or ""
    items.append((name, help))

    # recursively call for sub-commands with larger indent
    for subcommand in subcommands.values():
        if subcommand.get("hidden", False):
            continue
        items.extend(_commands_from_info(subcommand, indent_level + 1))

    return items


def show_command_tree(
    ctx: click.Context,
    param: click.Parameter,
    value: Any,
) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma: no cover

    info = ctx.to_info_dict()
    subcommands = info.get("command", {}).get("commands", {})  # skips top-level

    items = []
    for subcommand in subcommands.values():
        if subcommand.get("hidden", False):
            continue
        items.extend(_commands_from_info(subcommand, 0))

    if items:
        markup_mode = DEFAULT_MARKUP_MODE
        if not rich or markup_mode is None:  # pragma: no cover
            formatter = ctx.make_formatter()
            formatter.section(SUBCOMMAND_TITLE)
            formatter.write_dl(items)
            content = formatter.getvalue().rstrip("\n")
            click.echo(content)
        else:
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
