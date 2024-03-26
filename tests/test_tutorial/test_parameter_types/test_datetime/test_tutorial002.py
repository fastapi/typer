import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.datetime import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app, ["1969-10-29"])
    assert result.exit_code == 0
    assert "Launch will be at: 1969-10-29 00:00:00" in result.output


def test_usa_weird_date_format():
    result = runner.invoke(app, ["10/29/1969"])
    assert result.exit_code == 0
    assert "Launch will be at: 1969-10-29 00:00:00" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
