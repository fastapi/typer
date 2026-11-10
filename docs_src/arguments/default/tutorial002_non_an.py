import random

import typer

app = typer.Typer()


def get_name():
    return random.choice(["Deadpool", "Rick", "Morty", "Hiro"])


@app.command()
def main(name: str = typer.Argument(default_factory=get_name)):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
