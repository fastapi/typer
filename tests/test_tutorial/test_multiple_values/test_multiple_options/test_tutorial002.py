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
    module_name = f"docs_src.multiple_values.multiple_options.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "The sum is 0" in result.output


def test_1_number(mod: ModuleType):
    result = runner.invoke(mod.app, ["--number", "2"])
    assert result.exit_code == 0
    assert "The sum is 2.0" in result.output


def test_2_number(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--number", "2", "--number", "3", "--number", "4.5"]
    )
    assert result.exit_code == 0
    assert "The sum is 9.5" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
