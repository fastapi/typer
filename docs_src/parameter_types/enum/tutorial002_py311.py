from enum import StrEnum

import typer
from typing_extensions import Annotated


class NeuralNetwork(StrEnum):
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
    typer.run(main)
