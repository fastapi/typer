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
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.bool.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "-f" in result.output
    assert "--force" in result.output
    assert "-F" in result.output
    assert "--no-force" in result.output


def test_force(mod: ModuleType):
    result = runner.invoke(mod.app, ["-f"])
    assert result.exit_code == 0
    assert "Forcing operation" in result.output


def test_no_force(mod: ModuleType):
    result = runner.invoke(mod.app, ["-F"])
    assert result.exit_code == 0
    assert "Not forcing" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
