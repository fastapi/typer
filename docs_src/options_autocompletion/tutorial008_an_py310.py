from typing import Annotated

import typer
from rich.console import Console

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]

err_console = Console(stderr=True)


def complete_user(args: list[str], incomplete: str):
    err_console.print(f"{args}")
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete):
            yield (user, help_text)


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        list[str],
        typer.Option(help="The user to say hi to.", autocompletion=complete_user),
    ] = ["World"],
):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
