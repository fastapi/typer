import subprocess
import sys

from typer.testing import CliRunner

from tests.test_completion.for_testing import (
    commands_help_tutorial001_async as async_mod,
)

app = async_mod.app

runner = CliRunner()


def test_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing user database" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "--force", "Simone"])
    assert result.exit_code == 0
    assert "Deleting user: Simone" in result.output


def test_delete_no_force():
    result = runner.invoke(app, ["delete", "Simone"])
    assert result.exit_code == 0
    assert "Are you sure you want to delete the user?" in result.output


def test_delete_all():
    result = runner.invoke(app, ["delete-all", "--force"])
    assert result.exit_code == 0
    assert "Deleting all users" in result.output


def test_delete_all_no_force():
    result = runner.invoke(app, ["delete-all"])
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users?" in result.output


def test_create():
    result = runner.invoke(app, ["create", "Simone"])
    assert result.exit_code == 0
    assert "Creating user: Simone" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", async_mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
