import typer

app = typer.Typer()


@app.command()
def create(username: str):
    """
    Create a [green]new[green/] user with username.
    """
    print(f"Creating user: {username}")


@app.command()
def delete(username: str):
    """
    Delete a user with [bold]username[/].
    """
    print(f"Deleting user: {username}")


@app.command()
def delete_all():
    """
    [red]Delete ALL users[/red] in the database.
    """
    print("Deleting all users")


if __name__ == "__main__":
    app()
