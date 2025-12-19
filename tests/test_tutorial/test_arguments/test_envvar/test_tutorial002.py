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
    module_name = f"docs_src.arguments.envvar.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Arguments" in result.output
    assert "env var: AWESOME_NAME, GOD_NAME" in result.output
    assert "default: World" in result.output


def test_call_arg(mod: ModuleType):
    result = runner.invoke(mod.app, ["Wednesday"])
    assert result.exit_code == 0
    assert "Hello Mr. Wednesday" in result.output


def test_call_env_var1(mod: ModuleType):
    result = runner.invoke(mod.app, env={"AWESOME_NAME": "Wednesday"})
    assert result.exit_code == 0
    assert "Hello Mr. Wednesday" in result.output


def test_call_env_var2(mod: ModuleType):
    result = runner.invoke(mod.app, env={"GOD_NAME": "Anubis"})
    assert result.exit_code == 0
    assert "Hello Mr. Anubis" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
