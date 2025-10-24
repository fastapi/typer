import typer
from typing_extensions import Annotated

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_user(incomplete: str):
    completion = []
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete):
            completion_item = (user, help_text)
            completion.append(completion_item)
    return completion


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        str, typer.Option(help="The user to say hi to.", autocompletion=complete_user)
    ] = "World",
):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
