import os
import subprocess
import sys
from pathlib import Path

from ..utils import skip_if_windows


@skip_if_windows
def test_docs_output_does_not_depend_on_the_locale_encoding(tmp_path: Path):
    """The written file must not go through the process locale encoding.

    Forcing an ASCII locale here stands in for the cp1252 default on Windows:
    under the locale encoding this raised UnicodeEncodeError on any help text
    holding a character that encoding cannot represent.
    """
    out_path = tmp_path / "docs.md"
    env = {
        **os.environ,
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
    }
    env.pop("LANG", None)
    env.pop("LC_CTYPE", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/non_ascii_help.py",
            "utils",
            "docs",
            "--output",
            str(out_path),
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert "✨" in out_path.read_text(encoding="utf-8")
    assert "café" in out_path.read_text(encoding="utf-8")
