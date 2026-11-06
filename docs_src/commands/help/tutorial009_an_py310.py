from typing import Annotated

import typer

app = typer.Typer(align_panel_columns=True)


@app.callback()
def main(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-V", help="Verbose output.", rich_help_panel="Global options"
        ),
    ] = False,
    config: Annotated[
        str,
        typer.Option(
            "--config", "-c", help="Config file.", rich_help_panel="Global options"
        ),
    ] = "",
):
    """Manage the project."""


@app.command(rich_help_panel="Core")
def run():
    """Run the project."""


@app.command(rich_help_panel="Core")
def build():
    """Build the project."""


@app.command(rich_help_panel="Utilities")
def clean():
    """Clean build artifacts."""


@app.command(rich_help_panel="Utilities")
def prune():
    """Prune old artifacts."""


if __name__ == "__main__":
    app()
