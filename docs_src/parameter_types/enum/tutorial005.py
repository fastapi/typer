from enum import Enum

import typer

NeuralNetwork = Enum("NeuralNetwork", {k: k for k in ["simple", "conv", "lstm"]})

app = typer.Typer()


@app.command()
def main(network: NeuralNetwork = typer.Option("simple", case_sensitive=False)):
    print(f"Training neural network of type: {network.value}")


if __name__ == "__main__":
    app()
