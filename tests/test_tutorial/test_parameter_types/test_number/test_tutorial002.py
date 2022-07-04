import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.number import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_invalid_id():
    result = runner.invoke(app, ["1002"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Error: Invalid value for 'ID': 1002 is not in the range 0<=x<=1000"
        in result.output
        or "Error: Invalid value for 'ID': 1002 is not in the valid range of 0 to 1000."
        in result.output
    )


def test_clamped():
    result = runner.invoke(app, ["5", "--rank", "11", "--score", "-5"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--rank is 10" in result.output
    assert "--score is 0" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
