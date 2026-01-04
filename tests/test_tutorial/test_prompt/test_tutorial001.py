import subprocess
import sys

from typer.testing import CliRunner

from docs_src.prompt import tutorial001_py39 as mod

runner = CliRunner()
app = mod.app


def test_cli():
    result = runner.invoke(app, input="Camila\n")
    assert result.exit_code == 0
    assert "What's your name?:" in result.output
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
