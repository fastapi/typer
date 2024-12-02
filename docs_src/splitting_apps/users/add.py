import typer

app = typer.Typer()


@app.command()
def add(name: str):
    typer.echo(f"Adding user: {name}")
