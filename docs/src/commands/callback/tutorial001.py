import typer

app = typer.Typer()
state = {"verbose": False}


@app.command()
def create(username: str):
    if state["verbose"]:
        typer.echo("About to create a user")
    typer.echo(f"Creating user: {username}")
    if state["verbose"]:
        typer.echo("Just created a user")


@app.command()
def delete(username: str):
    if state["verbose"]:
        typer.echo("About to delete a user")
    typer.echo(f"Deleting user: {username}")
    if state["verbose"]:
        typer.echo("Just deleted a user")


@app.callback()
def main(verbose: bool = False):
    """
    Manage users in the awesome CLI app.
    """
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()
