import subprocess
import sys
from unittest.mock import patch

import typer
from typer.testing import CliRunner

from docs_src.asynchronous import tutorial001 as async_mod

runner = CliRunner()

app = typer.Typer()
app.command()(async_mod.main)


@patch("importlib.util.find_spec")
def test_asyncio(mocker):
    mocker.side_effect = [True, None]
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World\n" in result.output


@patch("importlib.util.find_spec")
def test_asyncio_no_anyio(mocker):
    mocker.side_effect = [None, None]
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World\n" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", async_mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
