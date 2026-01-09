import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.one_or_multiple import tutorial001_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "create" in result.output


def test_command():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating user: Hiro Hamada" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
