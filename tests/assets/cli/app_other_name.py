import typer

application = typer.Typer()


@application.command()
def callback(name: str = "World"):
    typer.echo(f"Hello {name}")
