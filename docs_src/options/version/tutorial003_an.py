from typing import Optional

import typer
from typing_extensions import Annotated

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def name_callback(name: str):
    if name != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return name


def main(
    name: Annotated[str, typer.Option(callback=name_callback)],
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
