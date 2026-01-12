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
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.bool.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "-d" in result.output
    assert "--demo" in result.output


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Running in production" in result.output


def test_demo(mod: ModuleType):
    result = runner.invoke(mod.app, ["--demo"])
    assert result.exit_code == 0
    assert "Running demo" in result.output


def test_short_demo(mod: ModuleType):
    result = runner.invoke(mod.app, ["-d"])
    assert result.exit_code == 0
    assert "Running demo" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
