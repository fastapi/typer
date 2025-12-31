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
    module_name = f"docs_src.options.name.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_option_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--name" in result.output
    assert "TEXT" in result.output
    assert "--user-name" not in result.output


def test_call(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_call_no_args(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name"])
    assert result.exit_code != 0
    assert "Option '--name' requires an argument" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
