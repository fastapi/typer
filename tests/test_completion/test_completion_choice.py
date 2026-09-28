import os
import subprocess
import sys

from . import choice_example as mod


def test_script() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--name", "rick"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "rick" in result.stdout


def test_completion_choice_bash() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_CHOICE_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "choice_example.py --name mo",
            "COMP_CWORD": "2",
        },
    )
    assert result.returncode == 0
    assert "morty" in result.stdout
    assert "rick" not in result.stdout
