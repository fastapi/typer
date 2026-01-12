import subprocess
import sys

from typer.testing import CliRunner

from docs_src.parameter_types.index import tutorial001_py39 as mod

runner = CliRunner()
app = mod.app


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--age" in result.output
    assert "INTEGER" in result.output
    assert "--height-meters" in result.output
    assert "FLOAT" in result.output


def test_params():
    result = runner.invoke(
        app, ["Camila", "--age", "15", "--height-meters", "1.70", "--female"]
    )
    assert result.exit_code == 0
    assert "NAME is Camila, of type: <class 'str'>" in result.output
    assert "--age is 15, of type: <class 'int'>" in result.output
    assert "--height-meters is 1.7, of type: <class 'float'>" in result.output
    assert "--female is True, of type: <class 'bool'>" in result.output


def test_invalid():
    result = runner.invoke(app, ["Camila", "--age", "15.3"])
    assert result.exit_code != 0
    assert "Invalid value for '--age'" in result.output
    assert "'15.3' is not a valid integer" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
