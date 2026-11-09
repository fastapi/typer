import typer

app = typer.Typer()


@app.command(help="Create a new user with username.")
def create(username: str):
    """
    Some internal utility function to create.
    """
    print(f"Creating user: {username}")


@app.command(help="Delete a user with username.")
def delete(username: str):
    """
    Some internal utility function to delete.
    """
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
