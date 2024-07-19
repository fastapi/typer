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
            "tests/assets/cli/multi_app_cli.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "sub" in result.stdout
    assert "top" in result.stdout


def test_script_sub():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_cli.py",
            "run",
            "sub",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "hello" in result.stdout


def test_script_top():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_cli.py",
            "run",
            "top",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "top" in result.stdout


def test_script_sub_hello():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_cli.py",
            "run",
            "sub",
            "hello",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "sub hello" in result.stdout


def test_script_sub_bye():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_app_cli.py",
            "run",
            "sub",
            "bye",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "sub bye" in result.stdout
