import subprocess

from click.testing import CliRunner

from docs_src.using_click import tutorial003 as mod

runner = CliRunner()


def test_cli():
    result = runner.invoke(mod.typer_click_object, [])
    # TODO: when deprecating Click 7, remove second option
    assert "Error: Missing command" in result.stdout or "Usage" in result.stdout


def test_typer():
    result = runner.invoke(mod.typer_click_object, ["top"])
    assert "The Typer app is at the top level" in result.stdout


def test_click():
    result = runner.invoke(mod.typer_click_object, ["hello", "--name", "Camila"])
    assert "Hello Camila!" in result.stdout


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
