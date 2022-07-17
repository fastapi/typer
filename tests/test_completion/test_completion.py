import os
import subprocess
import sys
from pathlib import Path

from docs_src.first_steps import tutorial001 as mod


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
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    assert "_TUTORIAL001.PY_COMPLETE=complete_bash" in result.stdout


def test_install_completion():
    bash_completion_path: Path = Path.home() / ".bashrc"
    text = ""
    if bash_completion_path.is_file():  # pragma: nocover
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
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    new_text = bash_completion_path.read_text()
    bash_completion_path.write_text(text)
    assert "source" in new_text
    assert ".bash_completions/tutorial001.py.sh" in new_text
    assert "completion installed in" in result.stdout
    assert "Completion will take effect once you restart the terminal" in result.stdout


def test_completion_invalid_instruction():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "sourcebash",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode != 0
    assert "Invalid completion instruction." in result.stderr


def test_completion_source_bash():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_bash",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "complete -o default -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


def test_completion_source_invalid_shell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_xxx",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Shell xxx not supported." in result.stderr


def test_completion_source_invalid_instruction():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "explode_bash",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert 'Completion instruction "explode" not supported.' in result.stderr


def test_completion_source_zsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_zsh",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


def test_completion_source_fish():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_fish",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "complete --command tutorial001.py --no-files" in result.stdout


def test_completion_source_powershell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_powershell",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


def test_completion_source_pwsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_pwsh",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )
