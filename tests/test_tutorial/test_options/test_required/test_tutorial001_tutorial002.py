import importlib
import subprocess
import sys
from types import ModuleType

import pytest
import typer
import typer.core
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial002_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.required.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila"])
    assert result.exit_code != 0
    assert "Missing option '--lastname'" in result.output


def test_option_lastname(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila", "--lastname", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--lastname" in result.output
    assert "TEXT" in result.output
    assert "[required]" in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--lastname" in result.output
    assert "TEXT" in result.output
    assert "[required]" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
