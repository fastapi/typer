import importlib
import subprocess
import sys
from types import ModuleType

import pytest
import typer
from typer.testing import CliRunner

from ....utils import needs_py310

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
        pytest.param("tutorial002_an_py39"),
        pytest.param("tutorial002_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.bool.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--accept" in result.output
    assert "--reject" in result.output
    assert "--no-accept" not in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--accept" in result.output
    assert "--reject" in result.output
    assert "--no-accept" not in result.output


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "I don't know what you want yet" in result.output


def test_accept(mod: ModuleType):
    result = runner.invoke(mod.app, ["--accept"])
    assert result.exit_code == 0
    assert "Accepting!" in result.output


def test_reject(mod: ModuleType):
    result = runner.invoke(mod.app, ["--reject"])
    assert result.exit_code == 0
    assert "Rejecting!" in result.output


def test_invalid_no_accept(mod: ModuleType):
    result = runner.invoke(mod.app, ["--no-accept"])
    assert result.exit_code != 0
    assert "No such option: --no-accept" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
