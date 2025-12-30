import platform
import subprocess
import sys

import pytest
from typer.testing import CliRunner

import docs_src.printing.tutorial004_py39 as mod

app = mod.app

runner = CliRunner()


@pytest.mark.xfail(
    condition=((platform.system() == "Windows") and (sys.version_info < (3, 10))),
    reason="On Windows with Python 3.9, output is in stdout instead of stderr",
)
def test_cli():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert result.stdout == ""
    assert "Here is something written to standard error" in result.stderr


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
