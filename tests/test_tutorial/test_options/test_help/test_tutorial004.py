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
        pytest.param("tutorial004_py310"),
        pytest.param("tutorial004_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_call(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Hello Wade Wilson" in result.output


def test_help(monkeypatch, mod: ModuleType):
    # avoid default width of 80 for non-attached consoles during testing
    monkeypatch.setenv("COLUMNS", "200")
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--fullname" in result.output
    assert "TEXT" in result.output
    assert "[default: (Deadpoolio the amazing's name)]" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
