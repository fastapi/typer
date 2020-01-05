import typer


def main(in_prod: bool = typer.Option(True, " /--demo", " /-d")):
    if in_prod:
        typer.echo("Running in production")
    else:
        typer.echo("Running demo")


if __name__ == "__main__":
    typer.run(main)
