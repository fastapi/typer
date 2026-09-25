import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial006_py310"),
        pytest.param("tutorial006_an_py310"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_call(mod: ModuleType):
    result = runner.invoke(mod.app, ["src", "--token", "secret"])
    assert result.exit_code == 0


def test_help(mod: ModuleType, monkeypatch: pytest.MonkeyPatch):
    import typer.rich_utils as rich_utils

    monkeypatch.setattr(rich_utils, "MAX_WIDTH", 100)
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Build the project." in result.output
    assert "Source directory." in result.output
    assert "Destination directory." in result.output
    assert "Extra files." in result.output
    assert "API token." in result.output
    assert "Long value with an alias." in result.output
    assert "Mixed value." in result.output
    assert "Force." in result.output
    assert "Pretty." in result.output
    assert "Formal." in result.output
    assert "Output path." in result.output
    assert "Color." in result.output
    assert "Level." in result.output
    assert "Count." in result.output
    assert "Timeout." in result.output
    assert "Mode." in result.output
    assert "Home." in result.output
    assert "--alpha,--aleph" in result.output
    assert "--force" in result.output
    assert "--no-force" in result.output
    assert "-P" in result.output
    assert "PATH" in result.output
    assert "[0<=x<=5]" in result.output
    assert "[env var: HOME]" in result.output
    assert "[required]" in result.output
    assert "[default: (auto)]" in result.output
    # hidden option is not shown
    assert "--secret" not in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
