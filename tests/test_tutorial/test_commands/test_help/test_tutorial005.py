import importlib
import os
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.commands.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a new shiny user. ✨" in result.output
    assert "delete" in result.output
    assert "Delete a user with USERNAME." in result.output
    assert "Some internal utility function to create." not in result.output
    assert "Some internal utility function to delete." not in result.output


def test_help_create(mod: ModuleType):
    result = runner.invoke(mod.app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new shiny user. ✨" in result.output
    assert "The username to be created" in result.output
    assert "Learn more at the Typer docs website" in result.output
    assert "Some internal utility function to create." not in result.output


def test_help_delete(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "Delete a user with USERNAME." in result.output
    assert "The username to be deleted" in result.output
    assert "Force the deletion 💥" in result.output
    assert "Some internal utility function to delete." not in result.output


def test_create(mod: ModuleType):
    result = runner.invoke(mod.app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_delete(mod: ModuleType):
    result = runner.invoke(mod.app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert "Usage" in result.stdout
