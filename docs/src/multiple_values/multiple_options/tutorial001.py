from typing import List

import typer


def main(user: List[str] = typer.Option(None)):
    if not user:
        typer.echo("No provided users")
        raise typer.Abort()
    for u in user:
        typer.echo(f"Processing user: {u}")


if __name__ == "__main__":
    typer.run(main)
