"""Color constants for terminal output styling.

This module provides string constants for standard and bright terminal colors
that can be used with typer's styling functions like `typer.style()` and
`typer.secho()` for the `fg` (foreground) and `bg` (background) parameters.

Example:
    >>> import typer
    >>> typer.secho("Hello", fg=typer.colors.GREEN)
    >>> styled = typer.style("Error", fg=typer.colors.RED, bold=True)
"""

BLACK = "black"
RED = "red"
GREEN = "green"
YELLOW = "yellow"
BLUE = "blue"
MAGENTA = "magenta"
CYAN = "cyan"
WHITE = "white"

RESET = "reset"

BRIGHT_BLACK = "bright_black"
BRIGHT_RED = "bright_red"
BRIGHT_GREEN = "bright_green"
BRIGHT_YELLOW = "bright_yellow"
BRIGHT_BLUE = "bright_blue"
BRIGHT_MAGENTA = "bright_magenta"
BRIGHT_CYAN = "bright_cyan"
BRIGHT_WHITE = "bright_white"
