import importlib
import subprocess
import sys
from types import ModuleType

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial008_py39"),
        pytest.param("tutorial008_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.arguments.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Say hi to NAME very gently, like Dirk." in result.output
    assert "Arguments" not in result.output
    assert "[default: World]" not in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Say hi to NAME very gently, like Dirk." in result.output
    assert "Arguments" not in result.output
    assert "[default: World]" not in result.output


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
