import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial007_an as mod

app = mod.app

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a new user. ✨" in result.output
    assert "Utils and Configs" in result.output
    assert "config" in result.output
    assert "Configure the system. 🔧" in result.output


def test_create_help():
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "username" in result.output
    assert "The username to create" in result.output
    assert "Secondary Arguments" in result.output
    assert "lastname" in result.output
    assert "The last name of the new user" in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "Force the creation of the user" in result.output
    assert "Additional Data" in result.output
    assert "--age" in result.output
    assert "The age of the new user" in result.output
    assert "--favorite-color" in result.output
    assert "The favorite color of the new user" in result.output


def test_call():
    # Mainly for coverage
    result = runner.invoke(app, ["create", "Morty"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["config", "Morty"])
    assert result.exit_code == 0


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
