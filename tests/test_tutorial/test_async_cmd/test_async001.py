import subprocess
import sys

import pytest
import typer
from typer.testing import CliRunner

from docs_src.async_cmd import async001 as mod

runner = CliRunner()


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="typer support for async functions requires python3.7 or higher",
)
def test_cli():
    app = typer.Typer()
    app.command()(mod.main)
    result = runner.invoke(app, [])
    assert result.output == "Hello Async World\n"


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="typer support for async functions requires python3.7 or higher",
)
def test_execute():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.stdout == "Hello Async World\n"


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
