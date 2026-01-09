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
    module_name = f"docs_src.parameter_types.number.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Verbose level is 0" in result.output


def test_verbose_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--verbose"])
    assert result.exit_code == 0
    assert "Verbose level is 1" in result.output


def test_verbose_3(mod: ModuleType):
    result = runner.invoke(mod.app, ["--verbose", "--verbose", "--verbose"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_verbose_short_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["-v"])
    assert result.exit_code == 0
    assert "Verbose level is 1" in result.output


def test_verbose_short_3(mod: ModuleType):
    result = runner.invoke(mod.app, ["-v", "-v", "-v"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_verbose_short_3_condensed(mod: ModuleType):
    result = runner.invoke(mod.app, ["-vvv"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
