import sys
from types import ModuleType
from unittest.mock import MagicMock

from typer.testing import CliRunner

# Mock the gitlab module before importing the tutorial
_gitlab = ModuleType("gitlab")
_gitlab.Gitlab = MagicMock  # type: ignore[attr-defined]
_gitlab.__file__ = "gitlab/__init__.py"  # type: ignore[attr-defined]
sys.modules.setdefault("gitlab", _gitlab)

from docs_src.exceptions import tutorial005_py39 as mod  # noqa: E402

runner = CliRunner()


def test_pretty_exceptions_suppress():
    result = runner.invoke(mod.app)
    assert result.exit_code == 0


def test_script():
    result = runner.invoke(mod.app, ["--help"])
    assert "Usage" in result.stdout
