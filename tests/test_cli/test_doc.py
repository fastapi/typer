import os
import subprocess
import sys
from pathlib import Path


def test_doc():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests.assets.cli.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent.parent / "assets/cli/multiapp-docs.md"
    docs = docs_path.read_text()
    assert docs in result.stdout
    assert "**Arguments**" in result.stdout


def test_doc_output(tmp_path: Path):
    out_file: Path = tmp_path / "out.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests.assets.cli.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
            "--output",
            str(out_file),
        ],
        capture_output=True,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent.parent / "assets/cli/multiapp-docs.md"
    docs = docs_path.read_text()
    written_docs = out_file.read_text()
    assert docs in written_docs
    assert "Docs saved to:" in result.stdout


def test_doc_title_output(tmp_path: Path):
    out_file: Path = tmp_path / "out.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests.assets.cli.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
            "--title",
            "Awesome CLI",
            "--output",
            str(out_file),
        ],
        capture_output=True,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent.parent / "assets/cli/multiapp-docs-title.md"
    docs = docs_path.read_text()
    written_docs = out_file.read_text()
    assert docs in written_docs
    assert "Docs saved to:" in result.stdout


def test_doc_output_non_ascii(tmp_path: Path):
    # Docs must be written as UTF-8 regardless of the platform's default
    # encoding, otherwise non-ASCII help (e.g. emojis) crashes with a
    # UnicodeEncodeError on interpreters where the locale encoding is not UTF-8
    # (e.g. cp1252 on Windows).
    app_file: Path = tmp_path / "emoji_app.py"
    app_file.write_text(
        "import typer\n"
        "app = typer.Typer()\n\n\n"
        "@app.command()\n"
        "def hello(name: str):\n"
        '    """Say hello 👋 to someone."""\n'
        "    print(name)\n",
        encoding="utf-8",
    )
    out_file: Path = tmp_path / "out.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            str(app_file),
            "utils",
            "docs",
            "--name",
            "emoji",
            "--output",
            str(out_file),
        ],
        capture_output=True,
        encoding="utf-8",
        # Force a non-UTF-8 locale so the write path fails on the old behavior
        # on any platform (not only Windows).
        env={
            **os.environ,
            "PYTHONUTF8": "0",
            "LC_ALL": "C",
            "LANG": "C",
            "PYTHONIOENCODING": "utf-8",
        },
    )
    assert result.returncode == 0, result.stderr
    written_docs = out_file.read_text(encoding="utf-8")
    assert "👋" in written_docs
    assert "Docs saved to:" in result.stdout


def test_doc_no_rich():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests.assets.cli.multi_app_norich",
            "utils",
            "docs",
            "--name",
            "multiapp",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent.parent / "assets/cli/multiapp-docs.md"
    docs = docs_path.read_text()
    assert docs in result.stdout
    assert "**Arguments**" in result.stdout


def test_doc_not_existing():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "no_typer",
            "utils",
            "docs",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Could not import as Python module:" in result.stderr


def test_doc_no_typer():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/empty_script.py",
            "utils",
            "docs",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "No Typer app found" in result.stderr


def test_doc_file_not_existing():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "assets/cli/not_existing.py",
            "utils",
            "docs",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Not a valid file or Python module:" in result.stderr


def test_doc_html_output(tmp_path: Path):
    out_file: Path = tmp_path / "out.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests.assets.cli.rich_formatted_app",
            "utils",
            "docs",
            "--title",
            "Awesome CLI",
            "--output",
            str(out_file),
        ],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    docs_path: Path = (
        Path(__file__).parent.parent / "assets" / "cli" / "richformattedapp-docs.md"
    )
    docs = docs_path.read_text(encoding="utf-8")
    written_docs = out_file.read_text(encoding="utf-8")
    assert docs in written_docs
    assert "Docs saved to:" in result.stdout
