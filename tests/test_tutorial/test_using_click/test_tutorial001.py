import subprocess
import sys

from click.testing import CliRunner

from docs_src.using_click import tutorial001_py39 as mod

runner = CliRunner()


def test_help():
    result = runner.invoke(mod.hello, ["--help"])
    assert result.exit_code == 0
    assert (
        "Simple program that greets NAME for a total of COUNT times." in result.output
    )
    assert "--name" in result.output
    assert "--count" in result.output


def test_cli_prompt():
    result = runner.invoke(mod.hello, input="Camila\n")
    assert result.exit_code == 0
    assert "Your name: Camila" in result.stdout
    assert "Hello Camila!" in result.stdout


def test_cli_with_name():
    result = runner.invoke(mod.hello, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila!" in result.stdout


def test_cli_with_name_and_count():
    result = runner.invoke(mod.hello, ["--name", "Camila", "--count", "3"])
    assert result.exit_code == 0
    assert "Hello Camila!" in result.stdout
    assert result.stdout.count("Hello Camila!") == 3


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
