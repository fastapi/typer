import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.options import tutorial001 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "delete-all" in result.output
    assert "init" in result.output


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


def test_delete_all_force():
    result = runner.invoke(app, ["delete-all", "--force"])
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" not in result.output
    assert "Deleting all users" in result.output


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
