import importlib

import pytest
import typer


@pytest.fixture(autouse=True)
def reload_rich_utils():
    # Reloading the module as some configuration options are being loaded on first import only.
    importlib.reload(typer.rich_utils)
