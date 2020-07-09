import subprocess

from typer.testing import CliRunner

from docs_src.subcommands.callback_override import tutorial002 as mod

runner = CliRunner()

app = mod.app


def test_cli():
    result = runner.invoke(app, ["users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Running a users command" in result.output
    assert "Creating user: Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
