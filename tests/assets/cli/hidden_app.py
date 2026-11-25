import typer

internal_app = typer.Typer()


@internal_app.command()
def rebuild():
    """
    Rebuild the index
    """


app = typer.Typer()
app.add_typer(internal_app, name="internal", hidden=True)


@app.command()
def public():
    """
    Public command
    """


@app.command(hidden=True)
def secret():
    """
    Secret command
    """
