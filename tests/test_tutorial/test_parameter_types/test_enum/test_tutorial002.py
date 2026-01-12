import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

from tests.utils import needs_py311

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_an_py39"),
        pytest.param("tutorial002_py311", marks=needs_py311),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.enum.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_upper(mod: ModuleType):
    result = runner.invoke(mod.app, ["--network", "CONV"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_mix(mod: ModuleType):
    result = runner.invoke(mod.app, ["--network", "LsTm"])
    assert result.exit_code == 0
    assert "Training neural network of type: lstm" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
