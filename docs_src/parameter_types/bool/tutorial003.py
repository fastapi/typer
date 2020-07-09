import typer


def main(force: bool = typer.Option(False, "--force/--no-force", "-f/-F")):
    if force:
        typer.echo("Forcing operation")
    else:
        typer.echo("Not forcing")


if __name__ == "__main__":
    typer.run(main)
