import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from docs_src.exceptions import tutorial001 as mod

runner = CliRunner()


def test_traceback_rich():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "_TYPER_STANDARD_TRACEBACK": ""},
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "typer.run(main)" not in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr
    assert "name = 'morty'" in result.stderr


def test_standard_traceback_env_var():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "_TYPER_STANDARD_TRACEBACK": "1"},
    )
    assert "return get_command(self)(*args, **kwargs)" in result.stderr

    assert "typer.run(main)" in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr
    assert "name = 'morty'" not in result.stderr


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
