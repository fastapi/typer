import subprocess

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.multiple_options_with_multiple_values import (
    tutorial001_an as mod,
)

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Congratulations, you're debt-free!" in result.output


def test_borrow_1():
    result = runner.invoke(app, ["--borrow", "2.5", "Mark"])
    assert result.exit_code == 0
    assert "Borrowed 2.50 from Mark" in result.output
    assert "Total borrowed: 2.50" in result.output


def test_borrow_many():
    result = runner.invoke(
        app,
        [
            "--borrow",
            "2.5",
            "Mark",
            "--borrow",
            "5.25",
            "Sean",
            "--borrow",
            "1.75",
            "Wade",
        ],
    )
    assert result.exit_code == 0
    assert "Borrowed 2.50 from Mark" in result.output
    assert "Borrowed 5.25 from Sean" in result.output
    assert "Borrowed 1.75 from Wade" in result.output
    assert "Total borrowed: 9.50" in result.output


def test_invalid_borrow():
    result = runner.invoke(app, ["--borrow", "2.5"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Option '--borrow' requires 2 arguments" in result.output
        or "--borrow option requires 2 arguments" in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
