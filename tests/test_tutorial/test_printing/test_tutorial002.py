import subprocess
import sys
from unittest.mock import patch

from rich.console import Console  # noqa: TID251
from typer.testing import CliRunner

import docs_src.printing.tutorial002_py39 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli():
    console = Console(force_terminal=True, width=100)
    with patch("rich.get_console", return_value=console):
        result = runner.invoke(app)

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert result.exit_code == 0
    assert "*Alert!* *Portal gun* shooting! *" in normalized_output


def test_cli_without_formatting():
    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Alert! Portal gun shooting! 💥" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
