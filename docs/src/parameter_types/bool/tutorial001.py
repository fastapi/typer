import typer


def main(force: bool = typer.Option(False, "--force")):
    if force:
        typer.echo("Forcing operation")
    else:
        typer.echo("Not forcing")


if __name__ == "__main__":
    typer.run(main)
