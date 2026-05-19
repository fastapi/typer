import typer

app = typer.Typer()


def users():
    """
    Manage users in the app.
    """


users_app = typer.Typer(callback=users, name="users")
app.add_typer(users_app)


@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
