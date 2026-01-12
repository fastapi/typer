import importlib
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
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
        pytest.param("tutorial004_an_py39"),
        pytest.param("tutorial004_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.enum.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--network [simple|conv|lstm]" in result.output.replace("  ", "")


def test_main(mod):
    result = runner.invoke(mod.app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_invalid(mod: ModuleType):
    result = runner.invoke(mod.app, ["--network", "capsule"])
    assert result.exit_code != 0
    assert "Invalid value for '--network'" in result.output
    assert (
        "invalid choice: capsule. (choose from" in result.output
        or "'capsule' is not one of" in result.output
    )
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
