import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial003_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli():
    result = runner.invoke(app)

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert result.exit_code == 0
    assert (
        "*\n* Name * Item *\n*\n* Rick * Portal Gun *\n* Morty * Plumbus *\n*\n"
    ) in normalized_output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
