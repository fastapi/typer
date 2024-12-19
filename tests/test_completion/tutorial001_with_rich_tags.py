import typer

app = typer.Typer(help="Awesome CLI user manager.")


@app.command()
def create(username: str):
    """
    Create a [green]new[green/] user with USERNAME.
    """
    print(f"Creating user: {username}")


@app.command()
def delete(
    username: str,
    force: bool = typer.Option(
        ...,
        prompt="Are you sure you want to delete the user?",
        help="Force deletion without confirmation.",
    ),
):
    """
    Delete a user with [bold]USERNAME[/].

    If --force is not used, will ask for confirmation.
    """
    if force:
        print(f"Deleting user: {username}")
    else:
        print("Operation cancelled")


@app.command()
def delete_all(
    force: bool = typer.Option(
        ...,
        prompt="Are you sure you want to delete ALL users?",
        help="Force deletion without confirmation.",
    ),
):
    """
    [red]Delete ALL users[/red] in the database.

    If --force is not used, will ask for confirmation.
    """
    if force:
        print("Deleting all users")
    else:
        print("Operation cancelled")


@app.command()
def init():
    """
    Initialize the users database.
    """
    print("Initializing user database")


if __name__ == "__main__":
    app()
