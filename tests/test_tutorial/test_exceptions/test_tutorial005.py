import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from docs_src.exceptions import tutorial005 as mod

runner = CliRunner()


def test_traceback_rich_pretty_width():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_STANDARD_TRACEBACK": "",
            "PYTHONIOENCODING": "utf-8",
        },
    )

    assert "print(name + deep_dict_or_json + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "dict") to str' in result.stderr
    assert "name = 'morty'" in result.stderr


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
