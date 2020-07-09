import subprocess

from typer.testing import CliRunner

from docs_src.commands.callback import tutorial003 as mod

app = mod.app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Override callback, running a command" in result.output
    assert "Running a command" not in result.output
    assert "Creating user: Camila" in result.output


def test_for_coverage():
    mod.callback()


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
