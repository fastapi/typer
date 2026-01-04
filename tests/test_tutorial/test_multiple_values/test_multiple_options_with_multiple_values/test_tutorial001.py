import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

from ....utils import needs_py310

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.multiple_values.multiple_options_with_multiple_values.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Congratulations, you're debt-free!" in result.output


def test_borrow_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--borrow", "2.5", "Mark"])
    assert result.exit_code == 0
    assert "Borrowed 2.50 from Mark" in result.output
    assert "Total borrowed: 2.50" in result.output


def test_borrow_many(mod: ModuleType):
    result = runner.invoke(
        mod.app,
        [
            "--borrow",
            "2.5",
            "Mark",
            "--borrow",
            "5.25",
            "Sean",
            "--borrow",
            "1.75",
            "Wade",
        ],
    )
    assert result.exit_code == 0
    assert "Borrowed 2.50 from Mark" in result.output
    assert "Borrowed 5.25 from Sean" in result.output
    assert "Borrowed 1.75 from Wade" in result.output
    assert "Total borrowed: 9.50" in result.output


def test_invalid_borrow(mod: ModuleType):
    result = runner.invoke(mod.app, ["--borrow", "2.5"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Option '--borrow' requires 2 arguments" in result.output
        or "--borrow option requires 2 arguments" in result.output
    )


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
