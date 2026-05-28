import subprocess
import sys
from unittest.mock import patch

from rich.console import Console  # noqa: TID251
from typer.testing import CliRunner

import docs_src.printing.tutorial001_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli():
    console = Console(force_terminal=True, width=100)
    with patch("rich.get_console", return_value=console):
        result = runner.invoke(app)

    assert result.exit_code == 0

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output, squash_whitespaces=False)

    assert (
        "Here's the data\n"
        "*{*\n"
        "    *'name'*: *'Rick'*,\n"
        "    *'age'*: *42*,\n"
        "    *'items'*: *[*{*'name'*: *'Portal Gun'*}*, *{*'name'*: *'Plumbus'*}*]*,\n"
        "    *'active'*: *True*,\n"
        "    *'affiliation'*: *None*\n"
        "*}*\n"
    ) in normalized_output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
