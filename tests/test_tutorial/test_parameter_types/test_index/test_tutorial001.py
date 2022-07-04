import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.index import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--age INTEGER" in result.output
    assert "--height-meters FLOAT" in result.output


def test_params():
    result = runner.invoke(
        app, ["Camila", "--age", "15", "--height-meters", "1.70", "--female"]
    )
    assert result.exit_code == 0
    assert "NAME is Camila, of type: <class 'str'>" in result.output
    assert "--age is 15, of type: <class 'int'>" in result.output
    assert "--height-meters is 1.7, of type: <class 'float'>" in result.output
    assert "--female is True, of type: <class 'bool'>" in result.output


def test_invalid():
    result = runner.invoke(app, ["Camila", "--age", "15.3"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Error: Invalid value for '--age': '15.3' is not a valid integer"
        in result.output
        or "Error: Invalid value for '--age': 15.3 is not a valid integer"
        in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
