from typing import Literal

import typer


def main(network: Literal["simple", "conv", "lstm"] = "simple"):
    typer.echo(f"Training neural network of type: {network}")


if __name__ == "__main__":
    typer.run(main)
