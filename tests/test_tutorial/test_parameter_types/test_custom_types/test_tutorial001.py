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
    module_name = f"docs_src.parameter_types.custom_types.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0


def test_parse_custom_type(mod: ModuleType):
    result = runner.invoke(mod.app, ["0", "--custom-opt", "1"])
    assert "custom_arg is <CustomClass: value=00>" in result.output
    assert "custom-opt is <CustomClass: value=11>" in result.output


def test_parse_custom_type_with_default(mod: ModuleType):
    result = runner.invoke(mod.app, ["0"])
    assert "custom_arg is <CustomClass: value=00>" in result.output
    assert "custom-opt is <CustomClass: value=FooFoo>" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
