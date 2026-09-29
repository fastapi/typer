"""Regression: Argument help must coerce lazy str proxies (discussion #1953)."""

from __future__ import annotations

import typing as t
from typing import Annotated

import typer
from typer.testing import CliRunner

runner = CliRunner()


class LazyStr:
    """Minimal stand-in for Django gettext_lazy / similar str proxies."""

    def __init__(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return self._value

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._value, name)


def test_argument_help_accepts_lazy_str_proxy() -> None:
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def main(
        name: Annotated[
            str,
            typer.Argument(
                help=LazyStr("Lazy argument help"),  # type: ignore[arg-type]
                show_default=False,
            ),
        ] = "default",
        opt: Annotated[
            str,
            typer.Option(help=LazyStr("Lazy option help")),  # type: ignore[arg-type]
        ] = "x",
    ) -> None:
        raise NotImplementedError  # pragma: no cover

    assert str(LazyStr("Lazy argument help")) == "Lazy argument help"

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.exception
    assert "Lazy argument help" in result.output
    assert "Lazy option help" in result.output
