from typing import Optional

import typer

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def name_callback(name: str):
    if name != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return name


def main(
    name: str = typer.Option(..., callback=name_callback),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
