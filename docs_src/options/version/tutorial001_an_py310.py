from typing import Annotated

import typer

__version__ = "0.1.0"

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    name: Annotated[str, typer.Option()] = "World",
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback)
    ] = None,
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
