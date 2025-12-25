from enum import Enum
from typing import Annotated

import typer


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


app = typer.Typer()


@app.command()
def main(
    network: Annotated[
        NeuralNetwork, typer.Option(case_sensitive=False)
    ] = NeuralNetwork.simple,
):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    app()
