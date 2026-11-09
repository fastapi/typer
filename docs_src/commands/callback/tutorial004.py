import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    Manage users CLI app.

    Use it with the create command.

    A new user with the given NAME will be created.
    """


@app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
