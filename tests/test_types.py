from enum import Enum

import pytest

import typer
from typer import _click
from typer.testing import CliRunner

app = typer.Typer(context_settings={"token_normalize_func": str.lower})


class User(str, Enum):
    rick = "Rick"
    morty = "Morty"


@app.command()
def hello(name: User = User.rick) -> None:
    print(f"Hello {name.value}!")


@app.command()
def hello_all(names: list[str] = typer.Argument(["World"], envvar="NAMES")) -> None:
    for name in names:
        print(f"Hello {name}!")


runner = CliRunner()


def test_enum_choice() -> None:
    # This test is only for coverage of the new custom TyperChoice class
    result = runner.invoke(app, ["hello", "--name", "morty"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Hello Morty!" in result.output

    result = runner.invoke(app, ["hello", "--name", "Rick"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output

    result = runner.invoke(app, ["hello", "--name", "RICK"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output


def test_split_envvar_value(monkeypatch) -> None:
    # This will use split_envvar_value to produce two strings from the envvar
    monkeypatch.setenv("NAMES", "Rick   Morty")
    result = runner.invoke(app, ["hello-all"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output
    assert "Hello Morty!" in result.output


def test_float_range_open_bounds_with_clamp_not_allowed():
    with pytest.raises(TypeError, match="Clamping is not supported for open bounds."):
        _click.types.FloatRange(min=0.0, min_open=True, clamp=True)
