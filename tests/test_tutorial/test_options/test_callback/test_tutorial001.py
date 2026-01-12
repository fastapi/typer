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
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.callback.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_2(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "rick"])
    assert result.exit_code != 0
    assert "Invalid value for '--name'" in result.output
    assert "Only Camila is allowed" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
