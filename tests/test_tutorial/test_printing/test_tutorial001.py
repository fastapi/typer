import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial001_py39 as mod

app = mod.app

runner = CliRunner()


def test_cli():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert result.output == (
        "Here's the data\n"
        "{\n"
        "    'name': 'Rick',\n"
        "    'age': 42,\n"
        "    'items': [{'name': 'Portal Gun'}, {'name': 'Plumbus'}],\n"
        "    'active': True,\n"
        "    'affiliation': None\n"
        "}\n"
    )


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
