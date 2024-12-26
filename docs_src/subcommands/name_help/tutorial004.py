import typer

app = typer.Typer()


def old_callback():
    """
    Old callback help.
    """


users_app = typer.Typer(callback=old_callback)
app.add_typer(users_app, name="users")


@users_app.callback()
def users():
    """
    Manage users in the app.
    """


@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
