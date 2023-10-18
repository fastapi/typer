import typer

app = typer.Typer(help="Awesome CLI user manager.")


@app.command()
async def create(username: str):
    """
    Create a new user with USERNAME.
    """
    typer.echo(f"Creating user: {username}")


@app.command()
async def delete(
    username: str,
    # force: bool = typer.Option(False, "--force")
    force: bool = typer.Option(
        False,
        prompt="Are you sure you want to delete the user?",
        help="Force deletion without confirmation.",
    ),
):
    """
    Delete a user with USERNAME.

    If --force is not used, will ask for confirmation.
    """
    typer.echo(f"Deleting user: {username}" if force else "Operation cancelled")


@app.command()
async def delete_all(
    force: bool = typer.Option(
        False,
        prompt="Are you sure you want to delete ALL users?",
        help="Force deletion without confirmation.",
    )
):
    """
    Delete ALL users in the database.

    If --force is not used, will ask for confirmation.
    """

    typer.echo("Deleting all users" if force else "Operation cancelled")


@app.command()
async def init():
    """
    Initialize the users database.
    """
    typer.echo("Initializing user database")


if __name__ == "__main__":
    app()
