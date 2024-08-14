import typer

app = typer.Typer()


@app.command()
def create(username: str):
    """
    Create a user.
    """
    print(f"Creating user: {username}")


@app.command(deprecated=True)
def delete(username: str):
    """
    Delete a user.

    This is deprecated and will stop being supported soon.
    """
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
