from enum import Enum

import typer


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


def main(network: NeuralNetwork = NeuralNetwork.simple):
    typer.echo(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    typer.run(main)
