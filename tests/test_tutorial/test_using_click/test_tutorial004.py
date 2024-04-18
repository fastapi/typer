import subprocess
import sys

from click.testing import CliRunner

from docs_src.using_click import tutorial004 as mod

runner = CliRunner()


def test_cli():
    result = runner.invoke(mod.cli, [])
    assert "Usage" in result.stdout
    assert "dropdb" in result.stdout
    assert "sub" in result.stdout


def test_typer():
    result = runner.invoke(mod.cli, ["sub"])
    assert "Typer is now below Click, the Click app is the top level" in result.stdout


def test_click_initdb():
    result = runner.invoke(mod.cli, ["initdb"])
    assert "Initialized the database" in result.stdout


def test_click_dropdb():
    result = runner.invoke(mod.cli, ["dropdb"])
    assert "Dropped the database" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
