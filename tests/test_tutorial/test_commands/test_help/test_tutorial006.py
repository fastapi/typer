import os
import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial006_py39 as mod

app = mod.app

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a new user. ✨" in result.output
    assert "delete" in result.output
    assert "Delete a user. ❌" in result.output
    assert "Utils and Configs" in result.output
    assert "config" in result.output
    assert "Configure the system. ⚙" in result.output
    assert "Synchronize the system or something fancy like that. ♻" in result.output
    assert "Help and Others" in result.output
    assert "Get help with the system. ❓" in result.output
    assert "Report an issue. ❗" in result.output


def test_call():
    # Mainly for coverage
    result = runner.invoke(app, ["create", "Morty"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["delete", "Morty"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["config", "Morty"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["sync"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["help"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["report"])
    assert result.exit_code == 0


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert "Usage" in result.stdout
