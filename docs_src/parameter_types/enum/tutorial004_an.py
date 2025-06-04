from enum import Enum

import typer
from typing_extensions import Annotated

NeuralNetwork = Enum("NeuralNetwork", {k: k for k in ["simple", "conv", "lstm"]})


def main(
    network: Annotated[NeuralNetwork, typer.Option(case_sensitive=False)] = "simple",
):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    typer.run(main)
