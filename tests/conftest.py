from pathlib import Path

import pytest
import typer


@pytest.fixture(name="app_dir")
def patch_app_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(typer, "get_app_dir", lambda _app_name: str(tmp_path))
    return tmp_path
