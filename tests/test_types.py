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
def hello_option(name: User = User.rick) -> None:
    print(f"Hello {name.value}!")


@app.command()
def hello_argument(name: User) -> None:
    print(f"Hello {name.value}!")


@app.command()
def hello_no_choices(
    name: User = typer.Option(..., "--name", show_choices=False),
):
    print(f"Hello {name.value}!")


@app.command()
def hello_all(names: list[str] = typer.Argument(["World"], envvar="NAMES")) -> None:
    for name in names:
        print(f"Hello {name}!")


runner = CliRunner()


def test_enum_choice() -> None:
    result = runner.invoke(
        app, ["hello-option", "--name", "morty"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "Hello Morty!" in result.output

    result = runner.invoke(app, ["hello-option", "--name", "Rick"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output

    result = runner.invoke(app, ["hello-option", "--name", "RICK"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output

    result = runner.invoke(app, ["hello-no-choices", "--name", "RICK"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output

    result = runner.invoke(app, ["hello-argument", "RICK"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output


def test_enum_choice_repr() -> None:
    root_command = typer.main.get_command(app)
    command = root_command.commands["hello-option"]
    name_param = next(param for param in command.params if param.name == "name")
    assert repr(name_param.type).startswith("Choice([")


def test_enum_choice_help() -> None:
    result = runner.invoke(app, ["hello-argument", "--help"])
    assert result.exit_code == 0
    assert "{rick|morty}" in result.output

    result = runner.invoke(app, ["hello-option", "--help"])
    assert result.exit_code == 0
    assert "[rick|morty]" in result.output

    result = runner.invoke(app, ["hello-no-choices", "--help"])
    assert result.exit_code == 0
    assert "--name" in result.output
    assert "rick|morty" not in result.output


def test_enum_choice_missing_message() -> None:
    result = runner.invoke(app, ["hello-argument"])
    assert result.exit_code != 0
    assert "Missing argument" in result.output
    assert "Choose from:" in result.output
    assert "rick" in result.output
    assert "morty" in result.output


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
