import random

import typer


def get_name():
    return random.choice(["Deadpool", "Rick", "Morty", "Hiro"])


def main(name: str = typer.Argument(get_name)):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
