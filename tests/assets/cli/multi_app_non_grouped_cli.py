import typer

sub_app = typer.Typer()


@sub_app.command()
def hello():
    typer.echo("hello there")


@sub_app.command()
def bye():
    typer.echo("bye bye")


cli = typer.Typer()
cli.add_typer(sub_app)


@cli.command()
def top():
    typer.echo("top")
