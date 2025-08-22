from enum import Enum

import typer
from typer.testing import CliRunner

app = typer.Typer(context_settings={"token_normalize_func": str.lower})


class User(str, Enum):
    rick = "Rick"
    morty = "Morty"


@app.command()
def hello(name: User = User.rick) -> None:
    print(f"Hello {name.value}!")


runner = CliRunner()


def test_enum_choice() -> None:
    # This test is only for coverage of the new custom TyperChoice class
    result = runner.invoke(app, ["--name", "morty"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Hello Morty!" in result.output

    result = runner.invoke(app, ["--name", "Rick"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output

    result = runner.invoke(app, ["--name", "RICK"])
    assert result.exit_code == 0
    assert "Hello Rick!" in result.output
