import subprocess
import sys

from typer.testing import CliRunner

from docs_src.terminating import tutorial001_py39 as mod

runner = CliRunner()
app = mod.app


def test_cli():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User created: Camila" in result.output
    assert "Notification sent for new user: Camila" in result.output


def test_existing():
    result = runner.invoke(app, ["rick"])
    assert result.exit_code == 0
    assert "The user already exists" in result.output
    assert "Notification sent for new user" not in result.output


def test_existing_no_standalone():
    # Mainly for coverage
    result = runner.invoke(app, ["rick"], standalone_mode=False)
    assert result.exit_code == 0
    assert "The user already exists" in result.output
    assert "Notification sent for new user" not in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
