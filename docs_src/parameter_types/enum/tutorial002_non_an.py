from enum import StrEnum

import typer


class NeuralNetwork(StrEnum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


app = typer.Typer()


@app.command()
def main(
    network: NeuralNetwork = typer.Option(NeuralNetwork.simple, case_sensitive=False),
):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    app()
