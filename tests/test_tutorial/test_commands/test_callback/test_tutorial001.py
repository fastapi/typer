import subprocess
import sys

import pytest
import typer.core
from typer.testing import CliRunner

from docs_src.commands.callback import tutorial001_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Manage users in the awesome CLI app." in result.output
    assert "--verbose" in result.output
    assert "--no-verbose" in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Manage users in the awesome CLI app." in result.output
    assert "--verbose" in result.output
    assert "--no-verbose" in result.output


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_create_verbose():
    result = runner.invoke(app, ["--verbose", "create", "Camila"])
    assert result.exit_code == 0
    assert "Will write verbose output" in result.output
    assert "About to create a user" in result.output
    assert "Creating user: Camila" in result.output
    assert "Just created a user" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_delete_verbose():
    result = runner.invoke(app, ["--verbose", "delete", "Camila"])
    assert result.exit_code == 0
    assert "Will write verbose output" in result.output
    assert "About to delete a user" in result.output
    assert "Deleting user: Camila" in result.output
    assert "Just deleted a user" in result.output


def test_wrong_verbose():
    result = runner.invoke(app, ["delete", "--verbose", "Camila"])
    assert result.exit_code != 0
    assert "No such option: --verbose" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
