from enum import Enum

import typer


class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


app = typer.Typer()


@app.command()
def main(network: NeuralNetwork = NeuralNetwork.simple):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    app()
