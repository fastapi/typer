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
        pytest.param("tutorial005_py310"),
        pytest.param("tutorial005_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_call(mod: ModuleType):
    result = runner.invoke(mod.app, ["src"])
    assert result.exit_code == 0


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Source path." in result.output
    assert "Destination path." in result.output
    assert "Short flag." in result.output
    assert "Mixed value." in result.output
    assert "Long value." in result.output
    assert "source" in result.output
    assert "-a" in result.output
    assert "--mixed-long" in result.output
    assert "--alpha" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
