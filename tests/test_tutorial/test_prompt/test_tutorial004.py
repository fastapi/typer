import subprocess
import sys

from typer.testing import CliRunner

from docs_src.prompt import tutorial004_py39 as mod

runner = CliRunner()
app = mod.app


def test_cli():
    result = runner.invoke(app, input="World\n")
    assert result.exit_code == 0
    assert "Enter your name" in result.output
    assert "Hey there World!" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
