import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.callback import tutorial003_py39 as mod

app = mod.app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Override callback, running a command" in result.output
    assert "Running a command" not in result.output
    assert "Creating user: Camila" in result.output


def test_for_coverage():
    mod.callback()


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
