import subprocess
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.file import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    config_file.write_text("some settings\nsome more settings")
    result = runner.invoke(app, ["--config", f"{config_file}"])
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config line: some settings" in result.output
    assert "Config line: some more settings" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
