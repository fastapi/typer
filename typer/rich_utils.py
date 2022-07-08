# Extracted and modified from https://github.com/ewels/rich-click

import inspect
import sys
from os import getenv
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

import click
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, group
from rich.emoji import Emoji
from rich.highlighter import RegexHighlighter
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

# Default styles
STYLE_OPTION = "bold cyan"
STYLE_SWITCH = "bold green"
STYLE_METAVAR = "bold yellow"
STYLE_METAVAR_APPEND = "dim yellow"
STYLE_METAVAR_SEPARATOR = "dim"
STYLE_HEADER_TEXT = ""
STYLE_FOOTER_TEXT = ""
STYLE_USAGE = "yellow"
STYLE_USAGE_COMMAND = "bold"
STYLE_DEPRECATED = "red"
STYLE_HELPTEXT_FIRST_LINE = ""
STYLE_HELPTEXT = "dim"
STYLE_OPTION_HELP = ""
STYLE_OPTION_DEFAULT = "dim"
STYLE_OPTION_ENVVAR = "dim yellow"
STYLE_REQUIRED_SHORT = "red"
STYLE_REQUIRED_LONG = "dim red"
STYLE_OPTIONS_PANEL_BORDER = "dim"
ALIGN_OPTIONS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES = False
STYLE_OPTIONS_TABLE_LEADING = 0
STYLE_OPTIONS_TABLE_PAD_EDGE = False
STYLE_OPTIONS_TABLE_PADDING = (0, 1)
STYLE_OPTIONS_TABLE_BOX = ""
STYLE_OPTIONS_TABLE_ROW_STYLES = None
STYLE_OPTIONS_TABLE_BORDER_STYLE = None
STYLE_COMMANDS_PANEL_BORDER = "dim"
ALIGN_COMMANDS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES = False
STYLE_COMMANDS_TABLE_LEADING = 0
STYLE_COMMANDS_TABLE_PAD_EDGE = False
STYLE_COMMANDS_TABLE_PADDING = (0, 1)
STYLE_COMMANDS_TABLE_BOX = ""
STYLE_COMMANDS_TABLE_ROW_STYLES = None
STYLE_COMMANDS_TABLE_BORDER_STYLE = None
STYLE_ERRORS_PANEL_BORDER = "red"
ALIGN_ERRORS_PANEL: Literal["left", "center", "right"] = "left"
STYLE_ERRORS_SUGGESTION = "dim"
STYLE_ABORTED = "red"
_TERMINAL_WIDTH = getenv("TERMINAL_WIDTH")
MAX_WIDTH = int(_TERMINAL_WIDTH) if _TERMINAL_WIDTH else None
COLOR_SYSTEM: Optional[
    Literal["auto", "standard", "256", "truecolor", "windows"]
] = "auto"  # Set to None to disable colors
FORCE_TERMINAL = (
    True
    if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS")
    else None
)

# Fixed strings
HEADER_TEXT: Optional[str] = None
FOOTER_TEXT: Optional[str] = None
DEPRECATED_STRING = "(Deprecated) "
DEFAULT_STRING = "[default: {}]"
ENVVAR_STRING = "[env var: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = "[required]"
RANGE_STRING = " [{}]"
APPEND_METAVARS_HELP_STRING = "({})"
ARGUMENTS_PANEL_TITLE = "Arguments"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"
ERRORS_PANEL_TITLE = "Error"
ERRORS_SUGGESTION: Optional[
    str
] = None  # Default: Try 'cmd -h' for help. Set to False to disable.
ERRORS_EPILOGUE: Optional[str] = None
ABORTED_TEXT = "Aborted."

# Behaviours
SHOW_ARGUMENTS = False  # Show positional arguments
SHOW_METAVARS_COLUMN = True  # Show a column with the option metavar (eg. INTEGER)
APPEND_METAVARS_HELP = False  # Append metavar (eg. [TEXT]) after the help text
GROUP_ARGUMENTS_OPTIONS = False  # Show arguments with options instead of in own panel
OPTION_ENVVAR_FIRST = False  # Show env vars before option help text instead of avert
USE_MARKDOWN = False  # Parse help strings as markdown
USE_MARKDOWN_EMOJI = True  # Parse emoji codes in markdown :smile:
USE_RICH_MARKUP = False  # Parse help strings for rich markup (eg. [red]my text[/])
# Define sorted groups of panels to display subcommands
COMMAND_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {}
# Define sorted groups of panels to display options and arguments
OPTION_GROUPS: Dict[str, List[Dict[str, Union[str, Sequence[str]]]]] = {}
USE_CLICK_SHORT_HELP = False  # Use click's default function to truncate help text


# Rich regex highlighter
class OptionHighlighter(RegexHighlighter):
    """Highlights our special options."""

    highlights = [
        r"(^|\W)(?P<switch>\-\w+)(?![a-zA-Z0-9])",
        r"(^|\W)(?P<option>\-\-[\w\-]+)(?![a-zA-Z0-9])",
        r"(?P<metavar>\<[^\>]+\>)",
        r"(?P<usage>Usage: )",
    ]


highlighter = OptionHighlighter()


def _get_rich_console() -> Console:
    return Console(
        theme=Theme(
            {
                "option": STYLE_OPTION,
                "switch": STYLE_SWITCH,
                "metavar": STYLE_METAVAR,
                "metavar_sep": STYLE_METAVAR_SEPARATOR,
                "usage": STYLE_USAGE,
            }
        ),
        highlighter=highlighter,
        color_system=COLOR_SYSTEM,
        force_terminal=FORCE_TERMINAL,
        width=MAX_WIDTH,
    )


def _make_rich_rext(text: str, style: str = "") -> Union[Markdown, Text]:
    """Take a string, remove indentations, and return styled text.

    By default, return the text as a Rich Text with the request style.
    If USE_RICH_MARKUP is True, also parse the text for Rich markup strings.
    If USE_MARKDOWN is True, parse as Markdown.

    Only one of USE_MARKDOWN or USE_RICH_MARKUP can be True.
    If both are True, USE_MARKDOWN takes precedence.

    Args:
        text (str): Text to style
        style (str): Rich style to apply

    Returns:
        MarkdownElement or Text: Styled text object
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if USE_MARKDOWN:
        if USE_MARKDOWN_EMOJI:
            text = Emoji.replace(text)
        return Markdown(text, style=style)
    if USE_RICH_MARKUP:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))


@group()
def _get_help_text(
    obj: Union[click.Command, click.Group]
) -> Iterable[Union[Markdown, Text]]:
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as depreciated, the depreciated string will be prepended.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for

    Yields:
        Text or Markdown: Multiple styled objects (depreciated, usage)
    """
    # Prepend deprecated status
    if obj.deprecated:
        yield Text(DEPRECATED_STRING, style=STYLE_DEPRECATED)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if not USE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_rext(first_line.strip(), STYLE_HELPTEXT_FIRST_LINE)

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if len(remaining_paragraphs) > 0:
        if not USE_MARKDOWN:
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = "\n".join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = "\n\n".join(remaining_paragraphs)

        yield _make_rich_rext(remaining_lines, STYLE_HELPTEXT)


def _get_parameter_help(
    param: Union[click.Option, click.Argument, click.Parameter], ctx: click.Context
) -> Columns:
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if
    applicable.

    Args:
        param (click.Option or click.Argument): Option or argument to build help text
            for
        ctx (click.Context): Click Context object

    Returns:
        Columns: A columns element with multiple styled objects (help, default,
            required)
    """
    # import here to avoid cyclic imports
    from .core import TyperOption

    items: List[Union[Text, Markdown]] = []

    # Get the environment variable first

    envvar = getattr(param, "envvar", None)
    var_str = ""
    # https://github.com/pallets/click/blob/0aec1168ac591e159baf6f61026d6ae322c53aaf/src/click/core.py#L2720-L2726
    if envvar is None:
        if (
            getattr(param, "allow_from_autoenv", None)
            and getattr(ctx, "auto_envvar_prefix", None) is not None
            and param.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{param.name.upper()}"
    if envvar is not None:
        var_str = (
            envvar if isinstance(envvar, str) else ", ".join(str(d) for d in envvar)
        )

    # Environment variable BEFORE help text
    if getattr(param, "show_envvar", None) and OPTION_ENVVAR_FIRST:
        items.append(Text(ENVVAR_STRING.format(var_str), style=STYLE_OPTION_ENVVAR))

    # Main help text
    help_value: Union[str, None] = getattr(param, "help", None)
    if help_value:
        paragraphs = help_value.split("\n\n")
        # Remove single linebreaks
        if not USE_MARKDOWN:
            paragraphs = [
                x.replace("\n", " ").strip()
                if not x.startswith("\b")
                else "{}\n".format(x.strip("\b\n"))
                for x in paragraphs
            ]
        items.append(_make_rich_rext("\n".join(paragraphs).strip(), STYLE_OPTION_HELP))

    # Append metavar if requested
    if APPEND_METAVARS_HELP:
        metavar_str = param.make_metavar()
        # Do it ourselves if this is a positional argument
        if (
            isinstance(param, click.Argument)
            and param.name
            and metavar_str == param.name.upper()
        ):
            metavar_str = param.type.name.upper()
            metavar_str = param.type.name.upper()
        # Skip booleans
        if metavar_str != "BOOLEAN":
            metavar_str = metavar_str.replace("[", "").replace("]", "")
            items.append(
                Text(
                    APPEND_METAVARS_HELP_STRING.format(metavar_str),
                    style=STYLE_METAVAR_APPEND,
                    overflow="fold",
                )
            )

    # Environment variable AFTER help text
    if getattr(param, "show_envvar", None) and not OPTION_ENVVAR_FIRST:
        items.append(Text(ENVVAR_STRING.format(envvar), style=STYLE_OPTION_ENVVAR))

    if isinstance(param, TyperOption):
        if param.show_default:
            show_default_is_str = isinstance(param.show_default, str)
            default_value = param._extract_default(ctx=ctx)
            default_str = param._get_default_string(
                ctx=ctx,
                show_default_is_str=show_default_is_str,
                default_value=default_value,
            )
            items.append(
                Text(
                    DEFAULT_STRING.format(default_str),
                    style=STYLE_OPTION_DEFAULT,
                )
            )

    # Required?
    if param.required:
        items.append(Text(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def _make_command_help(help_text: str) -> Union[Text, Markdown]:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.

    Args:
        help_text (str): Help text

    Returns:
        Text or Markdown: Styled object
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if not USE_MARKDOWN and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_rext(paragraphs[0].strip(), STYLE_OPTION_HELP)


def rich_format_help(
    obj: Union[click.Command, click.Group],
    ctx: click.Context,
    formatter: click.HelpFormatter,
) -> None:
    """Print nicely formatted help text using rich.

    Based on original code from rich-cli, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for
        ctx (click.Context): Click Context object
        formatter (click.HelpFormatter): Click HelpFormatter object
    """
    console = _get_rich_console()
    # Header text if we have it
    if HEADER_TEXT:
        console.print(
            Padding(_make_rich_rext(HEADER_TEXT, STYLE_HEADER_TEXT), (1, 1, 0, 1))
        )

    # Print usage
    console.print(
        Padding(highlighter(obj.get_usage(ctx)), 1), style=STYLE_USAGE_COMMAND
    )

    # Print command / group help if we have some
    if obj.help:

        # Print with some padding
        console.print(
            Padding(
                Align(_get_help_text(obj), pad=False),
                (0, 1, 1, 1),
            )
        )

    # Look through OPTION_GROUPS for this command
    # stick anything unmatched into a default group at the end
    option_groups = OPTION_GROUPS.get(ctx.command_path, []).copy()
    option_groups.append({"options": []})
    argument_group_options = []

    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered
        # in usage, see:
        # https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if isinstance(param, click.Argument) and not SHOW_ARGUMENTS:
            continue

        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue

        # Already mentioned in a config option group
        for option_group in option_groups:
            if any([opt in option_group.get("options", []) for opt in param.opts]):
                break

        # No break, no mention - add to the default group
        else:
            if isinstance(param, click.Argument) and not GROUP_ARGUMENTS_OPTIONS:
                argument_group_options.append(param.opts[0])
            else:
                list_of_option_groups = option_groups[-1]["options"]
                assert isinstance(list_of_option_groups, list)
                list_of_option_groups.append(param.opts[0])

    # If we're not grouping arguments and we got some, prepend before default options
    if len(argument_group_options) > 0:
        extra_option_group = {
            "name": ARGUMENTS_PANEL_TITLE,
            "options": argument_group_options,
        }
        option_groups.insert(len(option_groups) - 1, extra_option_group)

    # Print each option group panel
    for option_group in option_groups:

        options_rows = []
        for opt in option_group.get("options", []):

            # Get the param
            for param in obj.get_params(ctx):
                if any([opt in param.opts]):
                    break
            # Skip if option is not listed in this group
            else:
                continue

            # Short and long form
            opt_long_strs = []
            opt_short_strs = []
            for idx, opt in enumerate(param.opts):
                opt_str = opt
                try:
                    opt_str += "/" + param.secondary_opts[idx]
                except IndexError:
                    pass
                if "--" in opt:
                    opt_long_strs.append(opt_str)
                else:
                    opt_short_strs.append(opt_str)

            # Column for a metavar, if we have one
            metavar = Text(style=STYLE_METAVAR, overflow="fold")
            metavar_str = param.make_metavar()

            # Do it ourselves if this is a positional argument
            if (
                isinstance(param, click.Argument)
                and param.name
                and metavar_str == param.name.upper()
            ):
                metavar_str = param.type.name.upper()

            # Skip booleans and choices (handled above)
            if metavar_str != "BOOLEAN":
                metavar.append(metavar_str)

            # Range - from
            # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706  # noqa: E501
            try:
                # skip count with default range type
                if (
                    isinstance(param.type, click.types._NumberRangeBase)
                    and isinstance(param, click.Option)
                    and not (
                        param.count and param.type.min == 0 and param.type.max is None
                    )
                ):
                    range_str = param.type._describe_range()
                    if range_str:
                        metavar.append(RANGE_STRING.format(range_str))
            except AttributeError:
                # click.types._NumberRangeBase is only in Click 8x onwards
                pass

            # Required asterisk
            required: Union[str, Text] = ""
            if param.required:
                required = Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)

            # Highlighter to make [ | ] and <> dim
            class MetavarHighlighter(RegexHighlighter):
                highlights = [
                    r"^(?P<metavar_sep>(\[|<))",
                    r"(?P<metavar_sep>\|)",
                    r"(?P<metavar_sep>(\]|>)$)",
                ]

            metavar_highlighter = MetavarHighlighter()

            rows = [
                required,
                highlighter(highlighter(",".join(opt_long_strs))),
                highlighter(highlighter(",".join(opt_short_strs))),
                metavar_highlighter(metavar),
                _get_parameter_help(param, ctx),
            ]

            # Remove metavar if specified in config
            if not SHOW_METAVARS_COLUMN:
                rows.pop(3)

            options_rows.append(rows)

        if len(options_rows) > 0:
            t_styles: Dict[str, Any] = {
                "show_lines": STYLE_OPTIONS_TABLE_SHOW_LINES,
                "leading": STYLE_OPTIONS_TABLE_LEADING,
                "box": STYLE_OPTIONS_TABLE_BOX,
                "border_style": STYLE_OPTIONS_TABLE_BORDER_STYLE,
                "row_styles": STYLE_OPTIONS_TABLE_ROW_STYLES,
                "pad_edge": STYLE_OPTIONS_TABLE_PAD_EDGE,
                "padding": STYLE_OPTIONS_TABLE_PADDING,
            }
            t_styles.update(option_group.get("table_styles", {}))  # type: ignore
            box_style = getattr(box, t_styles.pop("box"), None)

            options_table = Table(
                highlight=True,
                show_header=False,
                expand=True,
                box=box_style,
                **t_styles,
            )
            # Strip the required column if none are required
            if all([x[0] == "" for x in options_rows]):
                options_rows = [x[1:] for x in options_rows]
            for row in options_rows:
                options_table.add_row(*row)
            console.print(
                Panel(
                    options_table,
                    border_style=STYLE_OPTIONS_PANEL_BORDER,
                    title=option_group.get("name", OPTIONS_PANEL_TITLE),  # type: ignore
                    title_align=ALIGN_OPTIONS_PANEL,
                )
            )

    #
    # Groups only:
    # List click command groups
    #
    # if hasattr(obj, "list_commands"):
    if isinstance(obj, click.MultiCommand):
        # Look through COMMAND_GROUPS for this command
        # stick anything unmatched into a default group at the end
        cmd_groups = COMMAND_GROUPS.get(ctx.command_path, []).copy()
        cmd_groups.append({"commands": []})
        for command in obj.list_commands(ctx):
            for cmd_group in cmd_groups:
                if command in cmd_group.get("commands", []):
                    break
            else:
                commands: List[str] = cmd_groups[-1]["commands"]  # type: ignore
                commands.append(command)

        # Print each command group panel
        for cmd_group in cmd_groups:
            t_styles = {
                "show_lines": STYLE_COMMANDS_TABLE_SHOW_LINES,
                "leading": STYLE_COMMANDS_TABLE_LEADING,
                "box": STYLE_COMMANDS_TABLE_BOX,
                "border_style": STYLE_COMMANDS_TABLE_BORDER_STYLE,
                "row_styles": STYLE_COMMANDS_TABLE_ROW_STYLES,
                "pad_edge": STYLE_COMMANDS_TABLE_PAD_EDGE,
                "padding": STYLE_COMMANDS_TABLE_PADDING,
            }
            t_styles.update(cmd_group.get("table_styles", {}))  # type: ignore
            box_style = getattr(box, t_styles.pop("box"), None)

            commands_table = Table(
                highlight=False,
                show_header=False,
                expand=True,
                box=box_style,
                **t_styles,
            )
            # Define formatting in first column, as commands don't match highlighter
            # regex
            commands_table.add_column(style="bold cyan", no_wrap=True)
            for command in cmd_group.get("commands", []):
                # Skip if command does not exist
                if command not in obj.list_commands(ctx):
                    continue
                cmd = obj.get_command(ctx, command)
                if not cmd:
                    continue
                if cmd.hidden:
                    continue
                # Use the truncated short text as with vanilla text if requested
                if USE_CLICK_SHORT_HELP:
                    helptext = cmd.get_short_help_str()
                else:
                    # Use short_help function argument if used, or the full help
                    helptext = cmd.short_help or cmd.help or ""
                commands_table.add_row(command, _make_command_help(helptext))
            if commands_table.row_count > 0:
                title = cmd_group.get("name", COMMANDS_PANEL_TITLE)
                console.print(
                    Panel(
                        commands_table,
                        border_style=STYLE_COMMANDS_PANEL_BORDER,
                        title=title,  # type: ignore
                        title_align=ALIGN_COMMANDS_PANEL,
                    )
                )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(Padding(Align(highlighter(epilogue), pad=False), 1))

    # Footer text if we have it
    if FOOTER_TEXT:
        console.print(
            Padding(_make_rich_rext(FOOTER_TEXT, STYLE_FOOTER_TEXT), (1, 1, 0, 1))
        )


def rich_format_error(self: click.ClickException) -> None:
    """Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.

    Args:
        click.ClickException: Click exception to format.
    """
    console = _get_rich_console()
    ctx: Union[click.Context, None] = getattr(self, "ctx", None)
    if ctx is not None:
        console.print(ctx.get_usage())
    if ERRORS_SUGGESTION:
        console.print(ERRORS_SUGGESTION, style=STYLE_ERRORS_SUGGESTION)
    elif (
        ERRORS_SUGGESTION is None
        and ctx is not None
        and ctx.command.get_help_option(ctx) is not None
    ):
        console.print(
            "Try [blue]'{command} {option}'[/] for help.".format(
                command=ctx.command_path, option=ctx.help_option_names[0]
            ),
            style=STYLE_ERRORS_SUGGESTION,
        )

    console.print(
        Panel(
            highlighter(self.format_message()),
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
        )
    )
    if ERRORS_EPILOGUE:
        console.print(ERRORS_EPILOGUE)


def rich_abort_error() -> None:
    """Print richly formatted abort error."""
    console = _get_rich_console()
    console.print(ABORTED_TEXT, style=STYLE_ABORTED)
