import subprocess

from typer.testing import CliRunner

from docs_src.commands.context import tutorial004 as mod

app = mod.app

runner = CliRunner()


def test_1():
    result = runner.invoke(app, ["--name", "Camila", "--city", "Berlin"])
    assert result.exit_code == 0
    assert "Got extra arg: --name" in result.output
    assert "Got extra arg: Camila" in result.output
    assert "Got extra arg: --city" in result.output
    assert "Got extra arg: Berlin" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
