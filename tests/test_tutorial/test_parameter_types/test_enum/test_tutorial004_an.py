import subprocess
import sys

import pytest
import typer
from typer.testing import CliRunner

pytestmark = pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8")


runner = CliRunner()


@pytest.fixture(scope="module")
def mod():
    from docs_src.parameter_types.enum import tutorial004_an as mod

    return mod


@pytest.fixture(scope="module")
def app(mod):
    app = typer.Typer()
    app.command()(mod.main)
    return app


def test_help(app):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network [simple|conv|lstm]" in result.output.replace("  ", "")


def test_main(app):
    result = runner.invoke(app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_invalid(app):
    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code != 0
    assert (
        "Invalid value for '--network': invalid choice: capsule. (choose from"
        in result.output
        or "Invalid value for '--network': 'capsule' is not one of" in result.output
    )
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_script(mod):
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
