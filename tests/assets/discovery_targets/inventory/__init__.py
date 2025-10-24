"""Nested package used to exercise discovery of Typer groups."""

from __future__ import annotations

import typer

app = typer.Typer()


@app.command()
def summary() -> None:
    """Emit a fixed inventory summary value."""

    typer.echo("inventory summary: 2 items")
