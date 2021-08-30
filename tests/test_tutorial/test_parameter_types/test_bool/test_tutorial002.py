import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.bool import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--accept / --reject" in result.output
    assert "--no-accept" not in result.output


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "I don't know what you want yet" in result.output


def test_accept():
    result = runner.invoke(app, ["--accept"])
    assert result.exit_code == 0
    assert "Accepting!" in result.output


def test_reject():
    result = runner.invoke(app, ["--reject"])
    assert result.exit_code == 0
    assert "Rejecting!" in result.output


def test_invalid_no_accept():
    result = runner.invoke(app, ["--no-accept"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Error: No such option: --no-accept" in result.output
        or "Error: no such option: --no-accept" in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
