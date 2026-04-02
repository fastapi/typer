import os
import subprocess
import sys

from . import path_example as mod
from . import path_typergroup_example as typergroup_mod


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "path/to/deadpool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "deadpool" in result.stdout


def test_typergroup_script():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            typergroup_mod.__file__,
            "sub",
            "process",
            "--input",
            "/tmp/test",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0


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


def test_completion_path_zsh_empty():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_example.py ",
        },
    )
    assert result.returncode == 0
    assert "_arguments" not in result.stdout


def test_completion_path_zsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_example.py /tmp/some_part",
        },
    )
    assert result.returncode == 0
    assert "_arguments" not in result.stdout


def test_completion_typergroup_path_zsh_empty():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input ",
        },
    )
    assert result.returncode == 0
    assert "_arguments" not in result.stdout


def test_completion_typergroup_path_zsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input /tmp/test",
        },
    )
    assert result.returncode == 0
    assert "_arguments" not in result.stdout


def test_completion_typergroup_dir_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --output-dir ",
        },
    )
    assert result.returncode == 0
    assert "_path_files -/" in result.stdout


def test_completion_typergroup_flags_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --",
        },
    )
    assert result.returncode == 0
    assert "_arguments" in result.stdout
    assert "--input" in result.stdout
    assert "--count" in result.stdout


def test_completion_typergroup_path_bash_empty():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "path_typergroup_example.py sub process --input ",
            "COMP_CWORD": "4",
        },
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_completion_typergroup_path_bash_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "path_typergroup_example.py sub process --input /tmp/test",
            "COMP_CWORD": "4",
        },
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_completion_typergroup_flags_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "path_typergroup_example.py sub process --",
            "COMP_CWORD": "3",
        },
    )
    assert result.returncode == 0
    assert "--input" in result.stdout
    assert "--count" in result.stdout


def test_completion_typergroup_path_fish_is_args():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input /tmp/test",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
        },
    )
    assert result.returncode != 0


def test_completion_typergroup_path_fish_get_args():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input /tmp/test",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
        },
    )
    assert result.stdout.strip() == ""


def test_completion_typergroup_path_powershell_empty():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input ",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "",
        },
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_completion_typergroup_path_powershell_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", typergroup_mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_PATH_TYPERGROUP_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "path_typergroup_example.py sub process --input /tmp/test",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "/tmp/test",
        },
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""
