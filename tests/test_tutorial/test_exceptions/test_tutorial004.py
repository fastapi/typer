import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from docs_src.exceptions import tutorial004 as mod

runner = CliRunner()


def test_rich_pretty_exceptions_disable():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "_TYPER_STANDARD_TRACEBACK": ""},
    )
    assert "return get_command(self)(*args, **kwargs)" in result.stderr

    assert "app()" in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
