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
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.file.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(tmpdir, mod: ModuleType):
    binary_file = Path(tmpdir) / "config.txt"
    binary_file.write_bytes(b"la cig\xc3\xbce\xc3\xb1a trae al ni\xc3\xb1o")
    result = runner.invoke(mod.app, ["--file", f"{binary_file}"])
    binary_file.unlink()
    assert result.exit_code == 0
    assert "Processed bytes total:" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
