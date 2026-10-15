from enum import Enum
from pathlib import Path

import typer

app = typer.Typer(align_panel_columns=True, add_completion=False)


class Color(str, Enum):
    red = "red"
    green = "green"


@app.command()
def main(
    source: str = typer.Argument(..., help="Source directory."),
    dest: str = typer.Argument("dist", help="Destination directory."),
    extras: list[str] = typer.Argument([], help="Extra files."),
    token: str = typer.Option(
        ..., "--token", help="API token.", rich_help_panel="Required"
    ),
    verbose: bool = typer.Option(
        False, "-v", help="Verbose.", rich_help_panel="Basic flags"
    ),
    alpha: str = typer.Option(
        "",
        "--alpha",
        "--aleph",
        help="Long value with an alias.",
        rich_help_panel="Basic flags",
    ),
    mixed: str = typer.Option(
        "", "--mixed-long", "-m", help="Mixed value.", rich_help_panel="Basic flags"
    ),
    force: bool = typer.Option(
        False,
        "--force/--no-force",
        "-f",
        help="Force.",
        rich_help_panel="Negative flags",
    ),
    pretty: bool = typer.Option(
        False, "-p/-P", help="Pretty.", rich_help_panel="Negative flags"
    ),
    formal: bool = typer.Option(
        False, "--formal/--no-formal", help="Formal.", rich_help_panel="Negative flags"
    ),
    output: Path = typer.Option(
        Path("."),
        "--path",
        metavar="PATH",
        help="Output path.",
        rich_help_panel="Values",
    ),
    color: Color = typer.Option(
        Color.red, "--color", help="Color.", rich_help_panel="Values"
    ),
    level: int = typer.Option(
        1, "--level", min=0, max=5, help="Level.", rich_help_panel="Values"
    ),
    count: int = typer.Option(
        0, "--count", "-c", count=True, help="Count.", rich_help_panel="Values"
    ),
    timeout: int = typer.Option(
        30, "--timeout", help="Timeout.", show_default=True, rich_help_panel="Defaults"
    ),
    mode: str = typer.Option(
        "", "--mode", help="Mode.", show_default="auto", rich_help_panel="Defaults"
    ),
    home: str = typer.Option(
        "",
        "--home",
        envvar="HOME",
        show_envvar=True,
        help="Home.",
        rich_help_panel="Defaults",
    ),
    secret: str = typer.Option("", "--secret", hidden=True, help="Hidden."),
) -> None:
    """Build the project."""


if __name__ == "__main__":
    app()
