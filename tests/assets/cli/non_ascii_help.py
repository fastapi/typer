import typer

app = typer.Typer()


@app.command()
def greet(name: str = "World"):
    """Say hi to someone ✨ with café flair."""
    typer.echo(f"Hello {name}")  # pragma: no cover
