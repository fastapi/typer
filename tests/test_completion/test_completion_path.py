import os
import subprocess
import sys

from . import path_example as mod


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "path/to/deadpool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "deadpool" in result.stdout


def test_completion_path_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "path_example.py ",
            "COMP_CWORD": "2",
        },
    )
    assert result.returncode == 0
