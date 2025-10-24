from typing import List

import typer
from typing_extensions import Annotated

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_user(ctx: typer.Context, incomplete: str):
    users = ctx.params.get("user") or []
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete) and user not in users:
            yield (user, help_text)


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        List[str],
        typer.Option(help="The user to say hi to.", autocompletion=complete_user),
    ] = ["World"],
):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
