import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.commands.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
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


def test_help_create(mod: ModuleType):
    result = runner.invoke(mod.app, ["create", "--help"])
    assert result.exit_code == 0
    assert "create [OPTIONS] USERNAME" in result.output
    assert "Create a new user with USERNAME." in result.output


def test_help_delete(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "delete [OPTIONS] USERNAME" in result.output
    assert "Delete a user with USERNAME." in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "Force deletion without confirmation." in result.output


def test_help_delete_all(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete-all", "--help"])
    assert result.exit_code == 0
    assert "delete-all [OPTIONS]" in result.output
    assert "Delete ALL users in the database." in result.output
    assert "If --force is not used, will ask for confirmation." in result.output
    assert "[required]" in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "Force deletion without confirmation." in result.output


def test_help_init(mod: ModuleType):
    result = runner.invoke(mod.app, ["init", "--help"])
    assert result.exit_code == 0
    assert "init [OPTIONS]" in result.output
    assert "Initialize the users database." in result.output


def test_create(mod: ModuleType):
    result = runner.invoke(mod.app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_delete(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete", "Camila"], input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete the user? [y/n]:" in result.output
    assert "Deleting user: Camila" in result.output


def test_no_delete(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete", "Camila"], input="n\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete the user? [y/n]:" in result.output
    assert "Operation cancelled" in result.output


def test_delete_all(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete-all"], input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" in result.output
    assert "Deleting all users" in result.output


def test_no_delete_all(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete-all"], input="n\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" in result.output
    assert "Operation cancelled" in result.output


def test_init(mod: ModuleType):
    result = runner.invoke(mod.app, ["init"])
    assert result.exit_code == 0
    assert "Initializing user database" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
