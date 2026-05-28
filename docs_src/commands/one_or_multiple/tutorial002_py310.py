import typer

app = typer.Typer()


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.callback()
def callback():
    """
    Creates a single user Hiro Hamada.

    In the next version it will create 5 more users.
    """


if __name__ == "__main__":
    app()
