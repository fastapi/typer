import typer

app = typer.Typer(pretty_exceptions_suggest_on_error=True)


@app.command()
def create():
    typer.echo("Creating...")


@app.command()
def delete():
    typer.echo("Deleting...")


if __name__ == "__main__":
    app()
