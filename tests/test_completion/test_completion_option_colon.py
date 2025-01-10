import os
import subprocess
import sys

from . import colon_example as mod


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--name", "DeadPool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "DeadPool" in result.stdout


def test_completion_colon_bash_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "colon_example.py --name ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" in result.stdout


def test_completion_colon_bash_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "colon_example.py --name alpine ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_bash_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "colon_example.py --name alpine:hell ",
            "COMP_CWORD": "2",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" not in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_zsh_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name ",
        },
    )
    assert "alpine\\\\:hello" in result.stdout
    assert "alpine\\\\:latest" in result.stdout
    assert "nvidia/cuda\\\\:10.0-devel-ubuntu18.04" in result.stdout


def test_completion_colon_zsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine",
        },
    )
    assert "alpine\\\\:hello" in result.stdout
    assert "alpine\\\\:latest" in result.stdout
    assert "nvidia/cuda\\\\:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_zsh_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine:hell",
        },
    )
    assert "alpine\\\\:hello" in result.stdout
    assert "alpine\\\\:latest" not in result.stdout
    assert "nvidia/cuda\\\\:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_powershell_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name ",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" in result.stdout


def test_completion_colon_powershell_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_powershell_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine:hell",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine:hell",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" not in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_pwsh_all():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name",
        },
    )

    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" in result.stdout


def test_completion_colon_pwsh_partial():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


def test_completion_colon_pwsh_single():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COLON_EXAMPLE.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "colon_example.py --name alpine:hell",
            "_TYPER_COMPLETE_WORD_TO_COMPLETE": "alpine:hell",
        },
    )
    assert "alpine:hello" in result.stdout
    assert "alpine:latest" not in result.stdout
    assert "nvidia/cuda:10.0-devel-ubuntu18.04" not in result.stdout


# TODO: tests for complete_fish
