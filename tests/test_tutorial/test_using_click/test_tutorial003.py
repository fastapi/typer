import subprocess
import sys

from click.testing import CliRunner

from docs_src.using_click import tutorial003_py39 as mod

runner = CliRunner()


def test_cli():
    result = runner.invoke(mod.typer_click_object, [])
    assert "Missing command" in result.output


def test_help():
    result = runner.invoke(mod.typer_click_object, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "top" in result.output
    assert "hello" in result.output


def test_typer():
    result = runner.invoke(mod.typer_click_object, ["top"])
    assert "The Typer app is at the top level" in result.stdout


def test_click():
    result = runner.invoke(mod.typer_click_object, ["hello", "--name", "Camila"])
    assert "Hello Camila!" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
