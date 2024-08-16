import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_parse_pydantic_model():
    result = runner.invoke(
        app,
        [
            "--person.name",
            "Jeff",
            "--person.pet.name",
            "Lassie",
            "--person.pet.species",
            "dog",
        ],
    )
    assert (
        "name='Jeff' age=None pet=Pet(name='Lassie', species='dog') <class 'docs_src.parameter_types.pydantic.tutorial002.Person'>"
        in result.output
    )


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
