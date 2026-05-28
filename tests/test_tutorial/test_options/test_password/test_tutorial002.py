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
        pytest.param("tutorial002_py310"),
        pytest.param("tutorial002_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.password.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_option_password(mod: ModuleType):
    result = runner.invoke(mod.app, ["Camila", "--password", "secretpassword"])
    assert result.exit_code == 0
    assert "Hello Camila. Doing something very secure with password." in result.output
    assert "...just kidding, here it is, very insecure: secretpassword" in result.output


def test_option_password_prompt(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["Camila"], input="secretpassword\nsecretpassword\n"
    )
    assert result.exit_code == 0
    assert "Password: " in result.output
    assert "Password: secretpassword" not in result.output
    assert "Repeat for confirmation: " in result.output
    assert "Repeat for confirmation: secretpassword" not in result.output
    assert "Hello Camila. Doing something very secure with password." in result.output
    assert "...just kidding, here it is, very insecure: secretpassword" in result.output


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    output_without_double_spaces = strip_double_spaces(result.output)
    assert "--password TEXT [required]" in output_without_double_spaces


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
