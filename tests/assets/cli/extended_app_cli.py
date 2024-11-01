import typer

sub_sub_app = typer.Typer()


@sub_sub_app.command()
def sub_sub_command():
    typer.echo("sub_sub_command")


sub_app = typer.Typer()
sub_app.add_typer(sub_sub_app, name="sub")


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
