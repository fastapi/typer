from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(align_panel_columns=True, add_completion=False)


class Color(str, Enum):
    red = "red"
    green = "green"


@app.command()
def main(
    source: Annotated[str, typer.Argument(help="Source directory.")],
    dest: Annotated[str, typer.Argument(help="Destination directory.")] = "dist",
    extras: Annotated[list[str], typer.Argument(help="Extra files.")] = (),
    token: Annotated[
        str, typer.Option("--token", help="API token.", rich_help_panel="Required")
    ] = ...,
    verbose: Annotated[
        bool, typer.Option("-v", help="Verbose.", rich_help_panel="Basic flags")
    ] = False,
    alpha: Annotated[
        str,
        typer.Option(
            "--alpha",
            "--aleph",
            help="Long value with an alias.",
            rich_help_panel="Basic flags",
        ),
    ] = "",
    mixed: Annotated[
        str,
        typer.Option(
            "--mixed-long", "-m", help="Mixed value.", rich_help_panel="Basic flags"
        ),
    ] = "",
    force: Annotated[
        bool,
        typer.Option(
            "--force/--no-force",
            "-f",
            help="Force.",
            rich_help_panel="Negative flags",
        ),
    ] = False,
    pretty: Annotated[
        bool,
        typer.Option("-p/-P", help="Pretty.", rich_help_panel="Negative flags"),
    ] = False,
    formal: Annotated[
        bool,
        typer.Option(
            "--formal/--no-formal", help="Formal.", rich_help_panel="Negative flags"
        ),
    ] = False,
    output: Annotated[
        Path,
        typer.Option(
            "--path", metavar="PATH", help="Output path.", rich_help_panel="Values"
        ),
    ] = Path("."),
    color: Annotated[
        Color, typer.Option("--color", help="Color.", rich_help_panel="Values")
    ] = Color.red,
    level: Annotated[
        int,
        typer.Option("--level", min=0, max=5, help="Level.", rich_help_panel="Values"),
    ] = 1,
    count: Annotated[
        int,
        typer.Option(
            "--count", "-c", count=True, help="Count.", rich_help_panel="Values"
        ),
    ] = 0,
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout",
            help="Timeout.",
            show_default=True,
            rich_help_panel="Defaults",
        ),
    ] = 30,
    mode: Annotated[
        str,
        typer.Option(
            "--mode", help="Mode.", show_default="auto", rich_help_panel="Defaults"
        ),
    ] = "",
    home: Annotated[
        str,
        typer.Option(
            "--home",
            envvar="HOME",
            show_envvar=True,
            help="Home.",
            rich_help_panel="Defaults",
        ),
    ] = "",
    secret: Annotated[str, typer.Option("--secret", hidden=True, help="Hidden.")] = "",
) -> None:
    """Build the project."""


if __name__ == "__main__":
    app()
