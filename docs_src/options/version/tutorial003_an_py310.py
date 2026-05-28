from typing import Annotated

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
    return name


@app.command()
def main(
    name: Annotated[str, typer.Option(callback=name_callback)],
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
