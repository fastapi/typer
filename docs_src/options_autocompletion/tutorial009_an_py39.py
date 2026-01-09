from typing import Annotated

import typer
from click.core import Parameter
from rich.console import Console

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]

err_console = Console(stderr=True)


def complete_user(
    ctx: typer.Context, args: list[str], param: Parameter, incomplete: str
):
    err_console.print(f"{args}")
    previous_users = ctx.params.get(param.name) or []
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete) and user not in previous_users:
            yield (user, help_text)


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        list[str],
        typer.Option(help="The user to say hi to.", autocompletion=complete_user),
    ] = ["World"],
):
    for n in user:
        print(f"Hello {n}")


if __name__ == "__main__":
    app()
