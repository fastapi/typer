import subprocess
import sys

import pytest
from typer.testing import CliRunner

from docs_src.async_cmd import async002 as mod

app = mod.app

runner = CliRunner()


def test_command_sync():
    result = runner.invoke(app, ["sync"])
    assert result.output == "Hello Sync World\n"


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="typer support for async functions requires python3.7 or higher",
)
def test_command_async():
    result = runner.invoke(app, ["async"])
    assert result.output == "Hello Async World\n"


def test_execute_sync():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "sync"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert result.stdout == "Hello Sync World\n"


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="typer support for async functions requires python3.7 or higher",
)
def test_execute_async():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "async"],
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
