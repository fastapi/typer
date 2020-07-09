import subprocess

import typer
from typer.testing import CliRunner

from docs_src.options.help import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_call():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Wade Wilson" in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--fullname TEXT" in result.output
    assert "[default: Wade Wilson]" not in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
