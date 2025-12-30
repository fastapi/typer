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
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.arguments.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] [NAME]" in result.output
    assert "Arguments" in result.output
    assert "Who to greet" in result.output
    assert "[default: (Deadpoolio the amazing's name)]" in result.output


def test_call_arg(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
