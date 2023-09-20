import typer
from typing_extensions import Annotated, Literal

NeuralNetworkType = Literal["simple", "conv", "lstm"]


def main(
    network: Annotated[NeuralNetworkType, typer.Option(case_sensitive=False)] = "simple"
):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    typer.run(main)
