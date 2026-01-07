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
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.arguments.optional.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_call_no_arg(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code != 0
    assert "Missing argument 'NAME'." in result.output


def test_call_no_arg_standalone(mod: ModuleType):
    # Mainly for coverage
    result = runner.invoke(mod.app, standalone_mode=False)
    assert result.exit_code != 0


def test_call_no_arg_no_rich(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    # Mainly for coverage
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app)
    assert result.exit_code != 0
    assert "Error: Missing argument 'NAME'" in result.output


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
