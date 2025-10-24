"""Sample command module discovered by tests."""

from __future__ import annotations

import typer

app = typer.Typer()


@app.command()
def create(name: str) -> None:
    """Emit a greeting for the supplied user."""

    typer.echo(f"created user {name}")


@app.command()
def deactivate(name: str) -> None:
    """Report deactivated user."""

    typer.echo(f"deactivated user {name}")
