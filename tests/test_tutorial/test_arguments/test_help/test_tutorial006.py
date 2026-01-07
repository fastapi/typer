import importlib
import subprocess
import sys
from types import ModuleType

import typer
import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="app",
    params=[
        pytest.param("tutorial006_py39"),
        pytest.param("tutorial006_an_py39"),
    ],
)
def get_app(request: pytest.FixtureRequest):
    module_name = f"docs_src.arguments.help.{request.param}"
    mod = importlib.import_module(module_name)
    app = typer.Typer(rich_markup_mode=None)
    app.command()(mod.main)
    return app


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] [✨user✨]" in result.output
    assert "Arguments" in result.output
    assert "name" not in result.output
    assert "[default: World]" in result.output


def test_call_arg(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
