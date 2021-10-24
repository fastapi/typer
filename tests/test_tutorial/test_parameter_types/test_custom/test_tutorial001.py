import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.custom import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "JSON" in result.output


def test_main():
    result = runner.invoke(app, ['--data={"what_i_like":"Python"}'])
    assert result.exit_code == 0
    assert "You like Python? Me too!" in result.output


def test_invalid():
    result = runner.invoke(app, ["--data=Python"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option
    assert (
        "Error: Invalid value for '--data': Bad JSON: Expecting value: line 1 column 1 (char 0)"
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
