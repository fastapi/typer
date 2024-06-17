import os
import subprocess
import sys
from pathlib import Path

from docs_src.commands.index import tutorial001 as mod

from ..utils import needs_cleaning, needs_linux


@needs_linux
def test_show_completion_flag():
    result = subprocess.run(
        [
            "bash",
            "-c",
            "typer --show-completion",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    curr_shell_path = os.environ["SHELL"]
    # check for default user shell
    shell = "bash"
    if "zsh" in curr_shell_path:
        shell = "zsh"
    if "fish" in curr_shell_path:
        shell = "fish"
    if "pwsh" in curr_shell_path:
        shell = "pwsh"
    assert f"_TYPER_COMPLETE=complete_{shell}" in result.stdout


@needs_cleaning
@needs_linux
def test_install_completion_flag():
    # NOTE: This test causes side-effects at runtime on your system shell config
    curr_shell_path = os.environ["SHELL"]

    completion_path: Path = Path.home() / ".bashrc"
    if "zsh" in curr_shell_path:
        completion_path: Path = Path.home() / ".zshrc"
    if "fish" in curr_shell_path:
        completion_path: Path = Path.home() / ".config/fish/completions/"

    text = ""
    if completion_path.is_file():  # pragma: no cover
        text = completion_path.read_text()
    result = subprocess.run(
        [
            "bash",
            "-c",
            "typer --install-completion",
        ],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "SHELL": "/bin/bash", "_TYPER_COMPLETE_TESTING": "True"},
    )

    shell_config_file = completion_path.read_text()
    completion_path.write_text(text)

    if "bash" in curr_shell_path:
        # check .bashrc
        assert "source" in shell_config_file
        assert str(Path(".bash_completions/tutorial001.py.sh")) in shell_config_file
    if "zsh" in curr_shell_path:
        # check .zshrc
        assert (
            "\n\nautoload -Uz compinit\nzstyle ':completion:*' menu select\nfpath+=~/.zfunc\n"
            in shell_config_file
        )

    assert "completion installed in" in result.stdout
    assert "Completion will take effect once you restart the terminal" in result.stdout


def test_completion_invalid_instruction():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "sourcebash",
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
            "_TUTORIAL001.PY_COMPLETE": "source_bash",
        },
    )
    assert (
        "complete -o default -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


def test_completion_source_invalid_shell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_xxx",
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
            "_TUTORIAL001.PY_COMPLETE": "explode_bash",
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
            "_TUTORIAL001.PY_COMPLETE": "source_zsh",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


def test_completion_source_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_fish",
        },
    )
    assert "complete --command tutorial001.py --no-files" in result.stdout


def test_completion_source_powershell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_powershell",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


def test_completion_source_pwsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "source_pwsh",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )
