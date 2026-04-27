from typer import _click


def test_detect_program_name_submodule_path() -> None:
    class MainModule:
        __package__ = "example"

    program_name = _click.utils._detect_program_name(
        path="/tmp/cli.py",
        _main=MainModule(),
    )

    assert program_name == "python -m example.cli"
