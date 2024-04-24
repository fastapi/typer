import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_parse_pydantic_model():
    result = runner.invoke(app, ["1", "--user.id", "2", "--user.name", "John Doe"])
    assert "1 <class 'int'>" in result.output
    assert (
        "id=2 name='John Doe' <class 'docs_src.parameter_types.pydantic.tutorial001.User'>"
        in result.output
    )


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
