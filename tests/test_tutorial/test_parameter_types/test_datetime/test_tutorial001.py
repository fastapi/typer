import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.datetime import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]" in result.output


def test_main():
    result = runner.invoke(app, ["1956-01-31T10:00:00"])
    assert result.exit_code == 0
    assert "Interesting day to be born: 1956-01-31 10:00:00" in result.output
    assert "Birth hour: 10" in result.output


def test_invalid():
    result = runner.invoke(app, ["july-19-1989"])
    assert result.exit_code != 0
    assert (
        "Invalid value for 'BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]':"
        in result.stdout
    )
    # TODO: when deprecating Click 7, remove second option
    assert (
        "'july-19-1989' does not match the formats" in result.output
        or "invalid datetime format: july-19-1989. (choose from" in result.output
    )
    assert "%Y-%m-%d" in result.output
    assert "%Y-%m-%dT%H:%M:%S" in result.output
    assert "%Y-%m-%d %H:%M:%S" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
