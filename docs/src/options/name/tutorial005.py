import typer


def main(
    name: str = typer.Option(..., "--name", "-n"),
    formal: bool = typer.Option(False, "--formal", "-f"),
):
    if formal:
        typer.echo(f"Good day Ms. {name}.")
    else:
        typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
