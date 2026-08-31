from enum import Enum

import typer

app = typer.Typer()


class User(str, Enum):
    rick = "rick"
    morty = "morty"


@app.command()
def main(name: User = typer.Option(User.rick, "--name")):
    print(name.value)


if __name__ == "__main__":
    app()
