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
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.number.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--age" in result.output
    assert "INTEGER RANGE" in result.output
    assert "--score" in result.output
    assert "FLOAT RANGE" in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--age" in result.output
    assert "INTEGER RANGE" in result.output
    assert "--score" in result.output
    assert "FLOAT RANGE" in result.output


def test_params(mod: ModuleType):
    result = runner.invoke(mod.app, ["5", "--age", "20", "--score", "90"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--age is 20" in result.output
    assert "--score is 90.0" in result.output


def test_invalid_id(mod: ModuleType):
    result = runner.invoke(mod.app, ["1002"])
    assert result.exit_code != 0
    assert (
        "Invalid value for 'ID': 1002 is not in the range 0<=x<=1000." in result.output
    )


def test_invalid_age(mod: ModuleType):
    result = runner.invoke(mod.app, ["5", "--age", "15"])
    assert result.exit_code != 0
    assert "Invalid value for '--age'" in result.output
    assert "15 is not in the range x>=18" in result.output


def test_invalid_score(monkeypatch: pytest.MonkeyPatch, mod: ModuleType):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(mod.app, ["5", "--age", "20", "--score", "100.5"])
    assert result.exit_code != 0
    assert "Invalid value for '--score'" in result.output
    assert "100.5 is not in the range x<=100." in result.output


def test_negative_score(mod: ModuleType):
    result = runner.invoke(mod.app, ["5", "--age", "20", "--score", "-5"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--age is 20" in result.output
    assert "--score is -5.0" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
