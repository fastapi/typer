from enum import StrEnum

import typer

app = typer.Typer()


class User(StrEnum):
    rick = "rick"
    morty = "morty"


@app.command()
def main(name: User = typer.Option(User.rick, "--name", case_sensitive=False)):
    print(name.value)


if __name__ == "__main__":
    app()
