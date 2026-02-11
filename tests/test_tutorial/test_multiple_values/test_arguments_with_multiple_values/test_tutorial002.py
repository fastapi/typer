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
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = (
        f"docs_src.multiple_values.arguments_with_multiple_values.{request.param}"
    )
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAMES]..." in result.output
    assert "Arguments" in result.output
    assert "[default: Harry, Hermione, Ron]" in result.output


def test_defaults(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Hello Harry" in result.output
    assert "Hello Hermione" in result.output
    assert "Hello Ron" in result.output


def test_invalid_args(mod: ModuleType):
    result = runner.invoke(mod.app, ["Draco", "Hagrid"])
    assert result.exit_code != 0
    assert "Argument 'names' takes 3 values" in result.output


def test_valid_args(mod: ModuleType):
    result = runner.invoke(mod.app, ["Draco", "Hagrid", "Dobby"])
    assert result.exit_code == 0
    assert "Hello Draco" in result.stdout
    assert "Hello Hagrid" in result.stdout
    assert "Hello Dobby" in result.stdout


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
