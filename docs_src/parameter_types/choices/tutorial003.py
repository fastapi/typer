import typer
from typing_extensions import Literal

NeuralNetworkType = Literal["simple", "conv", "lstm"]


def main(network: NeuralNetworkType = "simple"):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    typer.run(main)
