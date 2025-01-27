import typer
from typing_extensions import Literal


def main(network: Literal["simple", "conv", "lstm"] = typer.Option("simple")):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    typer.run(main)
