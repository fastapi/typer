import typer

valid_users = ["Camila", "Carlos", "Sebastian"]


def complete_user(incomplete: str):
    completion = []
    for user in valid_users:
        if user.startswith(incomplete):
            completion.append(user)
    return completion


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
