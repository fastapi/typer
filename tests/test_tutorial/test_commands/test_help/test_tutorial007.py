import importlib
import os
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

from ....utils import needs_py310

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial007_py39"),
        pytest.param("tutorial007_py310", marks=needs_py310),
        pytest.param("tutorial007_an_py39"),
        pytest.param("tutorial007_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.commands.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a new user. ✨" in result.output
    assert "Utils and Configs" in result.output
    assert "config" in result.output
    assert "Configure the system. ⚙" in result.output


def test_create_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["create", "--help"])
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


def test_call(mod: ModuleType):
    # Mainly for coverage
    result = runner.invoke(mod.app, ["create", "Morty"])
    assert result.exit_code == 0
    result = runner.invoke(mod.app, ["config", "Morty"])
    assert result.exit_code == 0


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert "Usage" in result.stdout
