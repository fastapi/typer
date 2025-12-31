import importlib
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.file.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(tmpdir, mod: ModuleType):
    binary_file = Path(tmpdir) / "config.txt"
    if binary_file.exists():  # pragma: no cover
        binary_file.unlink()
    result = runner.invoke(mod.app, ["--file", f"{binary_file}"])
    text = binary_file.read_text(encoding="utf-8")
    binary_file.unlink()
    assert result.exit_code == 0
    assert "Binary file written" in result.output
    assert "some settings" in text
    assert "la cigüeña trae al niño" in text


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
