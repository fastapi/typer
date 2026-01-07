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
    module_name = f"docs_src.options.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Say hi to NAME, optionally with a --lastname." in result.output
    assert "If --formal is used, say hi very formally." in result.output
    assert "Last name of person to greet." in result.output
    assert "Say hi formally." in result.output


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_option_lastname(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila", "--lastname", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_formal(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila", "--lastname", "Gutiérrez", "--formal"])
    assert result.exit_code == 0
    assert "Good day Ms. Camila Gutiérrez." in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
