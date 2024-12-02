import typer

app = typer.Typer()


@app.command()
def delete(name: str):
    typer.echo(f"Deleting user: {name}")
