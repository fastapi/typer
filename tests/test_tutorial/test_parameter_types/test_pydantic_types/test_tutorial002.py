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
        pytest.param("tutorial002_py310"),
        pytest.param("tutorial002_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.pydantic_types.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0


def test_url_opt(mod: ModuleType):
    result = runner.invoke(mod.app, ["--url-opt", "https://typer.tiangolo.com"])
    assert result.exit_code == 0
    assert "url_opt: https://typer.tiangolo.com" in result.output


def test_url_opt_invalid(mod: ModuleType):
    result = runner.invoke(mod.app, ["--url-opt", "invalid"])
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
