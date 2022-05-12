import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.number import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--age INTEGER RANGE" in result.output
    assert "--score FLOAT RANGE" in result.output


def test_params():
    result = runner.invoke(app, ["5", "--age", "20", "--score", "90"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--age is 20" in result.output
    assert "--score is 90.0" in result.output


def test_invalid_id():
    result = runner.invoke(app, ["1002"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option
    assert (
        (
            "Error: Invalid value for 'ID': 1002 is not in the range 0<=x<=1000."
            in result.output
        )
        or "Error: Invalid value for 'ID': 1002 is not in the valid range of 0 to 1000."
        in result.output
    )


def test_invalid_age():
    result = runner.invoke(app, ["5", "--age", "15"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Error: Invalid value for '--age': 15 is not in the range x>=18"
        in result.output
        or "Error: Invalid value for '--age': 15 is smaller than the minimum valid value 18."
        in result.output
    )


def test_invalid_score():
    result = runner.invoke(app, ["5", "--age", "20", "--score", "100.5"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Error: Invalid value for '--score': 100.5 is not in the range x<=100."
        in result.output
        or "Error: Invalid value for '--score': 100.5 is bigger than the maximum valid value 100."
        in result.output
    )


def test_negative_score():
    result = runner.invoke(app, ["5", "--age", "20", "--score", "-5"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--age is 20" in result.output
    assert "--score is -5.0" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
