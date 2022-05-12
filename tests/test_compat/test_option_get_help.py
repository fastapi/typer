import os
import subprocess

from typer.testing import CliRunner

from tests.assets import compat_click7_8 as mod

runner = CliRunner()


def test_hidden_option():
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Say hello" in result.output
    assert "--name" not in result.output
    assert "/lastname" in result.output
    assert "TEST_LASTNAME" in result.output
    assert "(dynamic)" in result.output


def test_coverage_call():
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Hello John Doe, it seems you have 42" in result.output


def test_completion():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPAT_CLICK7_8.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "compat_click7_8.py --nickname ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    # TODO: when deprecating Click 7, remove second option
    assert "Jonny" in result.stdout or "_files" in result.stdout
