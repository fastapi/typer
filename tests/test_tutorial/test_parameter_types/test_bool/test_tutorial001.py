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
    module_name = f"docs_src.parameter_types.bool.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--force" in result.output
    assert "--no-force" not in result.output


def test_no_force(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Not forcing" in result.output


def test_force(mod: ModuleType):
    result = runner.invoke(mod.app, ["--force"])
    assert result.exit_code == 0
    assert "Forcing operation" in result.output


def test_invalid_no_force(mod: ModuleType):
    result = runner.invoke(mod.app, ["--no-force"])
    assert result.exit_code != 0
    assert "No such option: --no-force" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
