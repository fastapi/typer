import subprocess
import sys

import pytest
import typer
from typer.testing import CliRunner

from docs_src.parameter_types.enum import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


@pytest.mark.parametrize("interval", ["1M", "1m"])
def test_case(interval):
    result = runner.invoke(app, ["--interval", interval])
    assert result.exit_code == 0
    assert f"Found interval: {interval}" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
