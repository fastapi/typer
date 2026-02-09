import subprocess
import sys

import pytest
import typer
import typer.core
from typer.testing import CliRunner

from docs_src.terminating import tutorial003_py39 as mod

runner = CliRunner()
app = mod.app


def test_cli():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "New user created: Camila" in result.output


def test_root():
    result = runner.invoke(app, ["root"])
    assert result.exit_code == 1
    assert "The root user is reserved" in result.output
    assert "Aborted" in result.output


def test_root_no_standalone():
    # Mainly for coverage
    result = runner.invoke(app, ["root"], standalone_mode=False)
    assert result.exit_code == 1


def test_root_no_rich(monkeypatch: pytest.MonkeyPatch):
    # Mainly for coverage
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(app, ["root"])
    assert result.exit_code == 1
    assert "The root user is reserved" in result.output
    assert "Aborted!" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
