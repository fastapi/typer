import typer

app = typer.Typer(suggest_commands=True)


@app.command()
def create():
    typer.echo("Creating...")


@app.command()
def delete():
    typer.echo("Deleting...")


if __name__ == "__main__":
    app()
