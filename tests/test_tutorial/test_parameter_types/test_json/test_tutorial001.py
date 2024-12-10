import json
import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.json import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--user-info" in result.output
    assert "DICT" in result.output


def test_params():
    data = {"name": "Camila", "age": 15, "height_meters": 1.7, "female": True}
    result = runner.invoke(
        app,
        [
            "--user-info",
            json.dumps(data),
        ],
    )
    assert result.exit_code == 0
    assert result.output.strip() == (f"User Info: {json.dumps(data)}")


def test_invalid():
    result = runner.invoke(app, ["--user-info", "Camila"])
    assert result.exit_code != 0
    assert "Expecting value: line 1 column 1 (char 0)" in result.exc_info[1].args[0]


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
