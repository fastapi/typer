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
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.enum.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--groceries" in result.output
    assert "[Eggs|Bacon|Cheese]" in result.output
    assert "default: Eggs, Cheese" in result.output


def test_call_no_arg(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Buying groceries: Eggs, Cheese" in result.output


def test_call_single_arg(mod: ModuleType):
    result = runner.invoke(mod.app, ["--groceries", "Bacon"])
    assert result.exit_code == 0
    assert "Buying groceries: Bacon" in result.output


def test_call_multiple_arg(mod: ModuleType):
    result = runner.invoke(mod.app, ["--groceries", "Eggs", "--groceries", "Bacon"])
    assert result.exit_code == 0
    assert "Buying groceries: Eggs, Bacon" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
