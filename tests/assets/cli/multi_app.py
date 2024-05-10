import typer

sub_app = typer.Typer()

variable = "Some text"


@sub_app.command(rich_help_panel="Greet")
def hello(name: str = "World", age: int = typer.Option(0, help="The age of the user")):
    """
    Say Hello
    """
    typer.echo(f"Hello {name}")


@sub_app.command(rich_help_panel="Greet")
def hi(user: str = typer.Argument("World", help="The name of the user to greet")):
    """
    Say Hi
    """


@sub_app.command(rich_help_panel="Farewell")
def bye():
    """
    Say bye
    """
    typer.echo("sub bye")


app = typer.Typer(help="Demo App", epilog="The end")
app.add_typer(sub_app, name="sub")


@app.command(rich_help_panel="")
def top():
    """
    Top command
    """
    typer.echo("top")


@app.command(rich_help_panel="Commands")
def trivial():
    """
    Trivial command
    """
    typer.echo("trivial")
