from typing import Annotated, Literal

import typer

app = typer.Typer()


@app.command()
def main(
    network: Annotated[Literal["simple", "conv", "lstm"], typer.Option()] = "simple",
):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    app()
