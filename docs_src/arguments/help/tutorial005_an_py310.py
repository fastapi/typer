from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    name: Annotated[
        str,
        typer.Argument(
            help="Who to greet", show_default="Deadpoolio the amazing's name"
        ),
    ] = "Wade Wilson",
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
