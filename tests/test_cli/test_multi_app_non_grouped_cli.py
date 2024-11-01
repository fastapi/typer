import subprocess
import sys


def test_script_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_non_grouped_cli.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "top" in result.stdout


def test_script_top():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_non_grouped_cli.py",
            "run",
            "top",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "top" in result.stdout


def test_script_hello():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_non_grouped_cli.py",
            "run",
            "hello",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "hello there" in result.stdout


def test_script_bye():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_non_grouped_cli.py",
            "run",
            "bye",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
