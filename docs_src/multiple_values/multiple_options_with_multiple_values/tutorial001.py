from typing import List, Optional, Tuple

import typer


def main(users: Optional[List[Tuple[str, str]]] = typer.Option(None)):
    if not users:
        typer.echo("No provided users")
        raise typer.Abort()
    for firstname, lastname in users:
        typer.echo(f"Processing user: {lastname}, {firstname}")


if __name__ == "__main__":
    typer.run(main)
