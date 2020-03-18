import typer

app = typer.Typer()


@app.command()
def create(username: str):
    typer.echo(f"Creating user: {username}")


@app.command()
def delete(username: str):
    typer.echo(f"Deleting user: {username}")


@app.callback()
def main(ctx: typer.Context):
    """
    Manage users in the awesome CLI app.
    """
    typer.echo(f"About to execute command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
