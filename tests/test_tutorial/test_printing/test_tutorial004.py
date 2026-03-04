import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial004_py310 as mod

app = mod.app

runner = CliRunner()


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
