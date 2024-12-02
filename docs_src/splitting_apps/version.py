import typer

app = typer.Typer()


@app.command()
def version():
    typer.echo("My CLI Version 1.0")
