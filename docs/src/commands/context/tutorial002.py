import typer

app = typer.Typer()


@app.command()
def create(username: str):
    typer.echo(f"Creating user: {username}")


@app.command()
def delete(username: str):
    typer.echo(f"Deleting user: {username}")


@app.callback(invoke_without_command=True)
def main():
    """
    Manage users in the awesome CLI app.
    """
    typer.echo("Initializing database")


if __name__ == "__main__":
    app()
