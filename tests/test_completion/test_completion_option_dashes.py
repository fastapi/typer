import os
import subprocess
import sys

from . import dashes_example as mod


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--name", "DeadPool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "DeadPool" in result.stdout


def test_completion_dashes_bash_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "dashes_example.py --name ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" in result.stdout


def test_completion_dashes_bash_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "dashes_example.py --name alpine ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_bash_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "dashes_example.py --name alpine-latest ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" not in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_zsh_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name ",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" in result.stdout


def test_completion_dashes_zsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_zsh_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine-latest",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" not in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_powershell_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name ",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" in result.stdout


def test_completion_dashes_powershell_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_powershell_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine-latest",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine-latest",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" not in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_pwsh_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name",
        },
    )

    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" in result.stdout


def test_completion_dashes_pwsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" in result.stdout
    assert "something-else-666" not in result.stdout


def test_completion_dashes_pwsh_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_DASHES_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "dashes_example.py --name alpine-latest",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine-latest",
        },
    )
    assert "alpine-latest-666" in result.stdout
    assert "alpine-hello-666" not in result.stdout
    assert "something-else-666" not in result.stdout


# TODO: tests for complete_fish
