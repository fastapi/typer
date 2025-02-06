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
