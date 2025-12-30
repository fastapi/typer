import importlib
import subprocess
import sys
from types import ModuleType

import pytest


@pytest.fixture(
    name="module_paths",
    params=[
        "app02_py39",
        "app02_an_py39",
    ],
)
def get_modules_path(request: pytest.FixtureRequest) -> str:
    return f"docs_src.testing.{request.param}"


@pytest.fixture(name="main_mod")
def get_main_mod(module_paths: str) -> ModuleType:
    mod = importlib.import_module(f"{module_paths}.main")
    return mod


@pytest.fixture(name="test_mod")
def get_test_mod(module_paths: str) -> ModuleType:
    mod = importlib.import_module(f"{module_paths}.test_main")
    return mod


def test_app02(test_mod: ModuleType):
    test_mod.test_app()


def test_script(main_mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", main_mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
