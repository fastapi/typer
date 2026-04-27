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
    module_name = f"docs_src.parameter_types.pydantic_types.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0


def test_tuple(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--server", "Example", "::1", "https://example.com"]
    )
    assert result.exit_code == 0
    assert "name: Example" in result.output
    assert "address: ::1" in result.output
    assert "url: https://example.com" in result.output


def test_tuple_invalid_ip(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--server", "Invalid", "invalid", "https://example.com"]
    )
    assert result.exit_code != 0
    assert "value is not a valid IPv4 or IPv6 address" in result.output


def test_tuple_invalid_url(mod: ModuleType):
    result = runner.invoke(mod.app, ["--server", "Invalid", "::1", "invalid"])
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
