import subprocess
import sys
from datetime import datetime

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.datetime import tutorial001_py310 as mod

runner = CliRunner()
app = mod.app


def test_type_repr():
    command = typer.main.get_command(app)
    birth_param = next(param for param in command.params if param.name == "birth")
    assert repr(birth_param.type) == "DateTime"


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]" in result.output


def test_main():
    result = runner.invoke(app, ["1956-01-31T10:00:00"])
    assert result.exit_code == 0
    assert "Interesting day to be born: 1956-01-31 10:00:00" in result.output
    assert "Birth hour: 10" in result.output


def test_main_datetime_object():
    result = runner.invoke(
        app, [], default_map={"birth": datetime(1956, 1, 31, 10, 0, 0)}
    )
    assert result.exit_code == 0
    assert "Interesting day to be born: 1956-01-31 10:00:00" in result.output
    assert "Birth hour: 10" in result.output


def test_invalid():
    result = runner.invoke(app, ["july-19-1989"])
    assert result.exit_code != 0
    assert (
        "Invalid value for 'BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]':"
        in result.output
    )
    assert "'july-19-1989' does not match the formats" in result.output
    assert "%Y-%m-%d" in result.output
    assert "%Y-%m-%dT%H:%M:%S" in result.output
    assert "%Y-%m-%d %H:%M:%S" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
