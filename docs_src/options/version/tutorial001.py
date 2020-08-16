from typing import Optional

import typer

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def main(
    name: str = typer.Option("World"),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback
    ),
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
