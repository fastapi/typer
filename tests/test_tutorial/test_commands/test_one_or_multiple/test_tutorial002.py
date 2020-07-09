import subprocess

from typer.testing import CliRunner

from docs_src.commands.one_or_multiple import tutorial002 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Creates a single user Hiro Hamada." in result.output
    assert "In the next version it will create 5 users more." in result.output
    assert "Commands:" in result.output
    assert "create" in result.output


def test_command():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating user: Hiro Hamada" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
