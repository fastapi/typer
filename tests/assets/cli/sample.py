import typer

app = typer.Typer()


@app.command()
def hello(name: str = "World", formal: bool = False):
    """
    Say hi
    """
    if formal:
        typer.echo(f"Good morning Ms. {name}")
    else:
        typer.echo(f"Hello {name}!")


@app.command()
def bye(friend: bool = False):
    """
    Say bye
    """
    if friend:
        typer.echo("Goodbye my friend")
    else:
        typer.echo("Goodbye")
