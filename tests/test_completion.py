import os
import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from first_steps import tutorial001 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_show_completion():
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"{sys.executable}  -m coverage run {mod.__file__} --show-completion",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash"},
    )
    assert "_TUTORIAL001.PY_COMPLETE=complete-bash" in result.stdout


def test_install_completion():
    bash_completion_path: Path = Path.home() / ".bash_completion"
    text = ""
    if bash_completion_path.is_file():
        text = bash_completion_path.read_text()
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"{sys.executable} -m coverage run {mod.__file__} --install-completion",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash"},
    )
    new_text = bash_completion_path.read_text()
    bash_completion_path.write_text(text)
    assert "_TUTORIAL001.PY_COMPLETE=complete-bash" in new_text
    assert "completion installed in" in result.stdout
    assert "Completion will take effect once you restart the terminal." in result.stdout
