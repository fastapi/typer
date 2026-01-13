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
    module_name = f"docs_src.parameter_types.pydantic_types.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0


def test_url_list(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--url", "https://example.com", "--url", "https://example.org"]
    )
    assert result.exit_code == 0
    assert "https://example.com" in result.output
    assert "https://example.org" in result.output


def test_url_invalid(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--url", "invalid", "--url", "https://example.org"]
    )
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
