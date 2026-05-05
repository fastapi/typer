from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    names: Annotated[
        tuple[str, str, str], typer.Argument(help="Select 3 characters to play with")
    ] = ("Harry", "Hermione", "Ron"),
):
    for name in names:
        print(f"Hello {name}")


if __name__ == "__main__":
    app()
