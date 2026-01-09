import typer

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_user(ctx: typer.Context, incomplete: str):
    previous_users = ctx.params.get("name") or []
    for user, help_text in valid_completion_items:
        if user.startswith(incomplete) and user not in previous_users:
            yield (user, help_text)


app = typer.Typer()


@app.command()
def main(
    user: list[str] = typer.Option(
        ["World"], help="The user to say hi to.", autocompletion=complete_user
    ),
):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
