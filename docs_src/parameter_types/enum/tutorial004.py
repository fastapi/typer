from enum import Enum

import typer

NeuralNetwork = Enum("NeuralNetwork", {k: k for k in ["simple", "conv", "lstm"]})


def main(network: NeuralNetwork = typer.Option("simple", case_sensitive=False)):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    typer.run(main)
