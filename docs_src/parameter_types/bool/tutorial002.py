from typing import Optional

import typer


def main(accept: Optional[bool] = typer.Option(None, "--accept/--reject")):
    if accept is None:
        typer.echo("I don't know what you want yet")
    elif accept:
        typer.echo("Accepting!")
    else:
        typer.echo("Rejecting!")


if __name__ == "__main__":
    typer.run(main)
