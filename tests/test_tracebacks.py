import os
import subprocess
import sys
from pathlib import Path


def test_traceback_no_rich():
    file_path = Path(__file__).parent / "assets/type_error_no_rich.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "app()" in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr


def test_traceback_no_rich_short_disable():
    file_path = Path(__file__).parent / "assets/type_error_no_rich_short_disable.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "app()" in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr


def test_unmodified_traceback():
    file_path = Path(__file__).parent / "assets/type_error_normal_traceback.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )
    assert "morty" in result.stdout, "the call to the first app should work normally"
    assert "return callback(**use_params)" in result.stderr, (
        "calling outside of Typer should show the normal traceback, "
        "even after the hook is installed"
    )
    assert "typer.main.get_command(broken_app)()" in result.stderr
    assert "print(name + 3)" in result.stderr
    assert 'TypeError: can only concatenate str (not "int") to str' in result.stderr


def test_rich_exceptions_dont_truncate_code_on_wide_terminal():
    file_path = Path(__file__).parent / "assets/type_error_rich.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TERMINAL_WIDTH": "120",
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )

    assert (
        "# The line below will cause TypeError because you cannot concatenate string and integer."
        in result.stderr
    )


def test_rich_exceptions_wrap_words_on_small_width_terminal():
    file_path = Path(__file__).parent / "assets/type_error_rich.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "TERMINAL_WIDTH": "80",
            "TYPER_STANDARD_TRACEBACK": "",
            "_TYPER_STANDARD_TRACEBACK": "",
        },
    )

    # Long line is wrapped, so the full line is not in the output, but parts of it are.
    assert "# The line below will cause TypeError because you cannot" in result.stderr
    assert "concatenate string and integer." in result.stderr
    assert (
        "# The line below will cause TypeError because you cannot concatenate string and integer."
        not in result.stderr
    )
