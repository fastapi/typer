import typer
from typer import _click


@_click.group()
def cli():
    pass


@cli.command()
def initdb():
    _click.echo("Initialized the database")


@cli.command()
def dropdb():
    _click.echo("Dropped the database")


app = typer.Typer()


@app.command()
def sub():
    """
    A single-command Typer sub app
    """
    print("Typer is now below Click, the Click app is the top level")


typer_click_object = typer.main.get_command(app)

cli.add_command(typer_click_object, "sub")

if __name__ == "__main__":
    cli()
