import typer

app = typer.Typer()


def old_callback():
    """
    Old callback help.
    """


users_app = typer.Typer(callback=old_callback, name="exp-users", help="Explicit help.")


def new_users():
    """
    I have the highland! Create some users.
    """


app.add_typer(
    users_app,
    callback=new_users,
    name="cake-sith-users",
    help="Unlimited powder! Eh, users.",
)


@users_app.callback("call-users", help="Help from callback for users.")
def users():
    """
    Manage users in the app.
    """


@users_app.command()
def create(name: str):
    typer.echo(f"Creating user: {name}")


if __name__ == "__main__":
    app()
