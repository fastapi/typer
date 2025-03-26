import pathlib

from typer import main


def test_param_path_convertor() -> None:
    assert main.param_path_convertor(None) is None
    assert main.param_path_convertor("/foo") == pathlib.Path("/foo")
    # check that expanduser has been called.
    # If we start to run tests on windows, we will probably need to update this
    assert main.param_path_convertor("~/foo").as_posix().startswith("/")
