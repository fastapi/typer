from typer import _click


@_click.group()
def cli():
    pass


@_click.command()
def initdb():
    _click.echo("Initialized the database")


@_click.command()
def dropdb():
    _click.echo("Dropped the database")


cli.add_command(initdb)
cli.add_command(dropdb)


if __name__ == "__main__":
    cli()
