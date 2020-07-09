import typer

app = typer.Typer()


@app.command()
def found(name: str):
    typer.echo(f"Founding town: {name}")


@app.command()
def burn(name: str):
    typer.echo(f"Burning town: {name}")


if __name__ == "__main__":
    app()
