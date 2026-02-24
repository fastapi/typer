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
        pytest.param("tutorial006_py310"),
        pytest.param("tutorial006_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.arguments.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


@pytest.fixture(
    name="app",
    params=[
        pytest.param(None),
        pytest.param("rich"),
    ],
)
def get_app(mod: ModuleType, request: pytest.FixtureRequest) -> typer.Typer:
    rich_markup_mode = request.param
    app = typer.Typer(rich_markup_mode=rich_markup_mode)
    app.command()(mod.main)
    return app


def test_help(app):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] [✨user✨]" in result.output
    assert "Arguments" in result.output
    assert "name" not in result.output
    assert "[default: World]" in result.output


def test_call_arg(app):
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
