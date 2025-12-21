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
    module_name = f"docs_src.commands.options.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "delete-all" in result.output
    assert "init" in result.output


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


def test_delete_all_force(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete-all", "--force"])
    assert result.exit_code == 0
    assert "Are you sure you want to delete ALL users? [y/n]:" not in result.output
    assert "Deleting all users" in result.output


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
