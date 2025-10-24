"""Nested module for discovery tests."""

from __future__ import annotations

import typer

app = typer.Typer()


@app.command()
def run(level: int = typer.Argument(1)) -> None:
    """Emit a diagnostic message with the requested audit level."""

    typer.echo(f"inventory audit level {level}")
