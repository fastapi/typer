from typing import Literal

import typer
from typing_extensions import Annotated


def main(
    network: Annotated[Literal["simple", "conv", "lstm"], typer.Option()] = "simple",
):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    typer.run(main)
