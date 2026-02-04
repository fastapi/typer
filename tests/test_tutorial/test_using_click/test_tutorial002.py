import subprocess
import sys

from click.testing import CliRunner

from docs_src.using_click import tutorial002_py39 as mod

runner = CliRunner()


def test_help():
    result = runner.invoke(mod.cli, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "initdb" in result.output
    assert "dropdb" in result.output


def test_initdb():
    result = runner.invoke(mod.cli, ["initdb"])
    assert "Initialized the database" in result.stdout


def test_dropdb():
    result = runner.invoke(mod.cli, ["dropdb"])
    assert "Dropped the database" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
