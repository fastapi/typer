import typer


def callback():
    typer.echo("Running a command")


app = typer.Typer(callback=callback)


@app.command()
def create(name: str):
    typer.echo(f"Creating user: {name}")


if __name__ == "__main__":
    app()
