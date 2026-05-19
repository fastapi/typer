import typer

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_user(incomplete: str):
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete):
            yield (user, help_text)


app = typer.Typer()


@app.command()
def main(
    user: str = typer.Option(
        "World", help="The user to say hi to.", autocompletion=complete_user
    ),
):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
