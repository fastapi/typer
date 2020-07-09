import typer

app = typer.Typer()


@app.command()
def create():
    typer.echo("Creating user: Hiro Hamada")


@app.callback()
def callback():
    pass


if __name__ == "__main__":
    app()
