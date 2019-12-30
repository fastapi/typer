import typer

app = typer.Typer()


@app.command()
def create(username: str):
    typer.echo(f"Creating user: {username}")


@app.command()
def delete(username: str):
    typer.echo(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
