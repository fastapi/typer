import sys
from types import ModuleType
from unittest.mock import MagicMock

from typer.testing import CliRunner

# Mock the gitlab module before importing the tutorial
_gitlab = ModuleType("gitlab")
_gitlab.Gitlab = MagicMock  # type: ignore[attr-defined]
_gitlab.__file__ = "gitlab/__init__.py"  # type: ignore[attr-defined]
sys.modules.setdefault("gitlab", _gitlab)

from docs_src.exceptions import tutorial005_py310 as mod  # noqa: E402

runner = CliRunner()

# There's no way to test a third-party package from PyPI. Also, the actual
# feature we use is part of Rich. We just pass the flag along. So here we test
# that the tutorial code runs without errors.

# Perhaps we could find some standard library module that throws a long
# traceback and test that instead, but for now this is probably good enough.


def test_pretty_exceptions_suppress():
    result = runner.invoke(mod.app)
    assert result.exit_code == 0


def test_script():
    result = runner.invoke(mod.app, ["--help"])
    assert "Usage" in result.stdout
