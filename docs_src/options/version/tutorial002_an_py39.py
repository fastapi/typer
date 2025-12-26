from typing import Annotated, Optional

import typer

__version__ = "0.1.0"

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def name_callback(name: str):
    if name != "Camila":
        raise typer.BadParameter("Only Camila is allowed")


@app.command()
def main(
    name: Annotated[str, typer.Option(callback=name_callback)],
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
