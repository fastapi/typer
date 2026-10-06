import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from docs_src.exceptions import tutorial005_py310 as mod

runner = CliRunner()


def test_pretty_exceptions_suppress():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )
    assert result.returncode != 0
    assert "URLError" in result.stderr
    # The user's own code should still appear with full context
    assert "urllib.request.urlopen" in result.stderr
    # Suppressed output is ~28 lines (only user's frame + collapsed library frames).
    # Without suppression it would be ~59 lines (all frames expanded with source context).
    # Threshold of 35 is generous enough for formatting changes but catches unsuppressed output.
    assert len(result.stderr.splitlines()) < 35


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
