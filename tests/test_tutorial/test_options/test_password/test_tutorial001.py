import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

from tests.utils import strip_double_spaces

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
        pytest.param("tutorial001_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.password.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_option_email(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila", "--email", "camila@example.com"])
    assert result.exit_code == 0
    assert "Hello Camila, your email is camila@example.com" in result.output


def test_option_email_prompt(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["Camila"], input="camila@example.com\ncamila@example.com\n"
    )
    assert result.exit_code == 0
    assert "Email: camila@example.com" in result.output
    assert "Repeat for confirmation: camila@example.com" in result.output
    assert "Hello Camila, your email is camila@example.com" in result.output


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    output_without_double_spaces = strip_double_spaces(result.output)
    assert "--email TEXT [required]" in output_without_double_spaces


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
