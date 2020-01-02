import typer

app = typer.Typer()


@app.command()
def create(username: str):
    typer.echo(f"Creating user: {username}")


@app.command()
def delete(
    username: str,
    force: bool = typer.Option(..., prompt="Are you sure you want to delete the user?"),
):
    if force:
        typer.echo(f"Deleting user: {username}")
    else:
        typer.echo("Operation cancelled")


@app.command()
def delete_all(
    force: bool = typer.Option(..., prompt="Are you sure you want to delete ALL users?")
):
    if force:
        typer.echo("Deleting all users")
    else:
        typer.echo("Operation cancelled")


@app.command()
def init():
    typer.echo("Initializing user database")


if __name__ == "__main__":
    app()
