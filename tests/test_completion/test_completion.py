import os
import subprocess
import sys
from pathlib import Path

from docs_src.typer_app import tutorial001_py39 as mod

from ..utils import needs_bash, needs_linux, requires_completion_permission


@needs_bash
@needs_linux
def test_show_completion():
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"'{sys.executable}' -m coverage run '{mod.__file__}' --show-completion",
        ],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    assert "_TUTORIAL001_PY39.PY_COMPLETE=complete_bash" in result.stdout


@needs_bash
@needs_linux
@requires_completion_permission
def test_install_completion():
    bash_completion_path: Path = Path.home() / ".bashrc"
    text = ""
    if bash_completion_path.is_file():  # pragma: no cover
        text = bash_completion_path.read_text()
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"'{sys.executable}' -m coverage run '{mod.__file__}' --install-completion",
        ],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )
    new_text = bash_completion_path.read_text()
    bash_completion_path.write_text(text)
    assert "source" in new_text
    assert str(Path(".bash_completions/tutorial001_py39.py.sh")) in new_text
    assert "completion installed in" in result.stdout
    assert "Completion will take effect once you restart the terminal" in result.stdout


def test_completion_invalid_instruction():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "sourcebash",
        },
    )
    assert result.returncode != 0
    assert "Invalid completion instruction." in result.stderr


def test_completion_source_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_bash",
        },
    )
    assert (
        "complete -o default -F _tutorial001_py39py_completion tutorial001_py39.py"
        in result.stdout
    )


def test_completion_source_invalid_shell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_xxx",
        },
    )
    assert "Shell xxx not supported." in result.stderr


def test_completion_source_invalid_instruction():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "explode_bash",
        },
    )
    assert 'Completion instruction "explode" not supported.' in result.stderr


def test_completion_source_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_zsh",
        },
    )
    assert "compdef _tutorial001_py39py_completion tutorial001_py39.py" in result.stdout


def test_completion_source_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_fish",
        },
    )
    assert "complete --command tutorial001_py39.py --no-files" in result.stdout


def test_completion_source_powershell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_powershell",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001_py39.py -ScriptBlock $scriptblock"
        in result.stdout
    )


def test_completion_source_pwsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_PY39.PY_COMPLETE": "source_pwsh",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001_py39.py -ScriptBlock $scriptblock"
        in result.stdout
    )
