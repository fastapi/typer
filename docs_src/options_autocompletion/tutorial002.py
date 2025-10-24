import typer


def complete_user():
    return ["Camila", "Carlos", "Sebastian"]


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
