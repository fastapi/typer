import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial009_an_py310 as mod

app = mod.app

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Manage the project." in result.output
    assert "Global options" in result.output
    assert "--verbose" in result.output
    assert "--config" in result.output
    assert "Core" in result.output
    assert "Run the project." in result.output
    assert "Build the project." in result.output
    assert "Utilities" in result.output
    assert "Clean build artifacts." in result.output
    assert "Prune old artifacts." in result.output


def test_call():
    # Mainly for coverage
    assert runner.invoke(app, ["run"]).exit_code == 0
    assert runner.invoke(app, ["build"]).exit_code == 0
    assert runner.invoke(app, ["clean"]).exit_code == 0
    assert runner.invoke(app, ["prune"]).exit_code == 0


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
