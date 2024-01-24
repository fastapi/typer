import os
import subprocess
import sys

from typer._compat_utils import _get_click_major

from tests.assets import compat_arg_complete_click7_8 as mod


def test_arg_completion():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "E"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPAT_ARG_COMPLETE_CLICK7_8.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "compat_arg_complete_click7_8.py E",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Emma" in result.stdout
    if _get_click_major() > 7:
        assert "Emma is awesome." in result.stdout

    assert "ctx: compat_arg_complete_click7_8" in result.stderr
    assert "arg is: name" in result.stderr
    assert "incomplete is: E" in result.stderr
