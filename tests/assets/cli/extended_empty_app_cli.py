import typer

cli = typer.Typer()
sub_app = typer.Typer()
cli.add_typer(sub_app)


@sub_app.command()
def hello():
    typer.echo("hello there")


@sub_app.command()
def bye():
    typer.echo("bye bye")
