import subprocess

from typer.testing import CliRunner

from docs_src.commands.index import tutorial001 as mod

app = mod.app

runner = CliRunner()


def test_no_arg():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "Error: Missing argument 'NAME'." in result.output


def test_arg():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
