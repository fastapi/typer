import typer

app = typer.Typer()


@app.command()
def conquer(name: str):
    typer.echo(f"Conquering reign: {name}")


@app.command()
def destroy(name: str):
    typer.echo(f"Destroying reign: {name}")


if __name__ == "__main__":
    app()
