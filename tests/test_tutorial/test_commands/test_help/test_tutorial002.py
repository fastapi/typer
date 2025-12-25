import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial002_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a new user with USERNAME." in result.output
    assert "delete" in result.output
    assert "Delete a user with USERNAME." in result.output
    assert "Some internal utility function to create." not in result.output
    assert "Some internal utility function to delete." not in result.output


def test_help_create():
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new user with USERNAME." in result.output
    assert "Some internal utility function to create." not in result.output


def test_help_delete():
    result = runner.invoke(app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "Delete a user with USERNAME." in result.output
    assert "Some internal utility function to delete." not in result.output


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
