from typing import Literal

import typer

app = typer.Typer()


@app.command()
def main(network: Literal["simple", "conv", "lstm"] = typer.Option("simple")):
    print(f"Training neural network of type: {network}")


if __name__ == "__main__":
    app()
