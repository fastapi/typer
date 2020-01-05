import typer


def callback():
    typer.echo("Running a command")


app = typer.Typer(callback=callback)


@app.callback()
def new_callback():
    typer.echo("Override callback, running a command")


@app.command()
def create(name: str):
    typer.echo(f"Creating user: {name}")


if __name__ == "__main__":
    app()
