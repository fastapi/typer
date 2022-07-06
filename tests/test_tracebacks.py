import subprocess
from pathlib import Path


def test_traceback_rich():
    file_path = Path(__file__).parent / "assets/type_error_rich.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "typer.run(main)" in result.stderr
    assert "print(name + 3)" in result.stderr

    # TODO: when deprecating Python 3.6, remove second option
    assert (
        'TypeError: can only concatenate str (not "int") to str' in result.stderr
        or "TypeError: must be str, not int" in result.stderr
    )
    assert "name = 'morty'" in result.stderr


def test_traceback_no_rich():
    file_path = Path(__file__).parent / "assets/type_error_no_rich.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "typer.run(main)" in result.stderr
    assert "print(name + 3)" in result.stderr
    # TODO: when deprecating Python 3.6, remove second option
    assert (
        'TypeError: can only concatenate str (not "int") to str' in result.stderr
        or "TypeError: must be str, not int" in result.stderr
    )


def test_unmodified_traceback():
    file_path = Path(__file__).parent / "assets/type_error_normal_traceback.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "morty" in result.stdout, "the call to the first app should work normally"
    assert "return callback(**use_params)" in result.stderr, (
        "calling outside of Typer should show the normal traceback, "
        "even after the hook is installed"
    )
    assert "typer.main.get_command(broken_app)()" in result.stderr
    assert "print(name + 3)" in result.stderr
    # TODO: when deprecating Python 3.6, remove second option
    assert (
        'TypeError: can only concatenate str (not "int") to str' in result.stderr
        or "TypeError: must be str, not int" in result.stderr
    )
