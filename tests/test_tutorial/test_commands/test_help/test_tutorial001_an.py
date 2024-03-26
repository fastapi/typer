import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial001_an as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Awesome CLI user manager." in result.output
    assert "create" in result.output
    assert "Create a new user with USERNAME." in result.output
    assert "delete" in result.output
    assert "Delete a user with USERNAME." in result.output
    assert "delete-all" in result.output
    assert "Delete ALL users in the database." in result.output
    assert "init" in result.output
    assert "Initialize the users database." in result.output


def test_help_create():
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "create [OPTIONS] USERNAME" in result.output
    assert "Create a new user with USERNAME." in result.output


def test_help_delete():
    result = runner.invoke(app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "delete [OPTIONS] USERNAME" in result.output
    assert "Delete a user with USERNAME." in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "Force deletion without confirmation." in result.output


def test_help_delete_all():
    result = runner.invoke(app, ["delete-all", "--help"])
    assert result.exit_code == 0
    assert "delete-all [OPTIONS]" in result.output
    assert "Delete ALL users in the database." in result.output
    assert "If --force is not used, will ask for confirmation." in result.output
    assert "[required]" in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "Force deletion without confirmation." in result.output


def test_help_init():
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    assert "init [OPTIONS]" in result.output
    assert "Initialize the users database." in result.output


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"], input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete the user? [y/n]:" in result.output
    assert "Deleting user: Camila" in result.output


def test_no_delete():
    result = runner.invoke(app, ["delete", "Camila"], input="n\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete the user? [y/n]:" in result.output
    assert "Operation cancelled" in result.output


def test_delete_all():
    result = runner.invoke(app, ["delete-all"], input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" in result.output
    assert "Deleting all users" in result.output


def test_no_delete_all():
    result = runner.invoke(app, ["delete-all"], input="n\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" in result.output
    assert "Operation cancelled" in result.output


def test_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing user database" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
