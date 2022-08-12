import subprocess

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.options_with_multiple_values import tutorial001 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "No user provided" in result.output
    assert "Aborted" in result.output


def test_user_1():
    result = runner.invoke(app, ["--user", "Camila", "50", "yes"])
    assert result.exit_code == 0
    assert "The username Camila has 50 coins" in result.output
    assert "And this user is a wizard!" in result.output


def test_user_2():
    result = runner.invoke(app, ["--user", "Morty", "3", "no"])
    assert result.exit_code == 0
    assert "The username Morty has 3 coins" in result.output
    assert "And this user is a wizard!" not in result.output


def test_invalid_user():
    result = runner.invoke(app, ["--user", "Camila", "50"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Option '--user' requires 3 arguments" in result.output
        or "--user option requires 3 arguments" in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
