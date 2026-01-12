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
    module_name = f"docs_src.parameter_types.number.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_invalid_id(mod: ModuleType):
    result = runner.invoke(mod.app, ["1002"])
    assert result.exit_code != 0
    assert (
        "Invalid value for 'ID': 1002 is not in the range 0<=x<=1000" in result.output
    )


def test_clamped(mod: ModuleType):
    result = runner.invoke(mod.app, ["5", "--rank", "11", "--score", "-5"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--rank is 10" in result.output
    assert "--score is 0" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
