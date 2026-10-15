import typer

zeta = typer.Typer()


@zeta.command()
def hello():
    print("zeta")


alpha = typer.Typer()
