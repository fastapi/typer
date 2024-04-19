import os
import subprocess
import sys

from tests.assets import completion_argument as mod


def test_arg_completion():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "E"],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_ARGUMENT.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_argument.py E",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Emma" in result.stdout or "_files" in result.stdout
    assert "ctx: completion_argument" in result.stderr
    assert "arg is: name" in result.stderr
    assert "incomplete is: E" in result.stderr
