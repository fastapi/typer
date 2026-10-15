import subprocess
import sys
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from . import atomic_write_example as mod

runner = CliRunner()


def test_atomic_write(tmp_path: Path) -> None:
    original_content = "existing-content\n"
    output_file = tmp_path / "atomic-write-target.txt"
    output_file.write_text(original_content, encoding="utf-8")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "write-atomic",
            f"--config={output_file}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None

    # Halfway of writing the file, check that the original content is still there
    halfway_line = process.stdout.readline().strip()
    assert halfway_line == "halfway"
    assert output_file.read_text(encoding="utf-8") == original_content

    # Only at the end, the full new content is visible
    stdout, stderr = process.communicate(timeout=5)
    assert process.returncode == 0, stderr
    assert "written atomically" in stdout
    assert (
        output_file.read_text(encoding="utf-8")
        == "atomic-content-1\natomic-content-2\n"
    )


def test_atomic_binary_write(tmp_path: Path) -> None:
    output_file = tmp_path / "atomic-binary.bin"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "write-atomic-binary",
            f"--config={output_file}",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert "written binary atomically" in result.stdout
    assert output_file.read_bytes() == b"\x00\x01binary-atomic\n"


def test_atomic_api(tmp_path: Path) -> None:
    output_file = tmp_path / "atomic-api.txt"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "api-atomic",
            f"--config={output_file}",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert f"name={output_file}" in result.stdout
    assert "repr=<_io.TextIOWrapper" in result.stdout
    assert "entered=True" in result.stdout
    assert output_file.read_text(encoding="utf-8") == "atomic-api-done\n"


@pytest.mark.parametrize("lazy", [True, False], ids=["lazy", "eager"])
@pytest.mark.parametrize(
    "destination_exists", [True, False], ids=["existing", "missing"]
)
def test_atomic_write_callback_failure(
    tmp_path: Path, lazy: bool, destination_exists: bool
) -> None:
    original_content = "existing-content\n"
    output_file = tmp_path / "atomic-failure-target.txt"
    if destination_exists:
        output_file.write_text(original_content, encoding="utf-8")
    initial_entries = set(tmp_path.iterdir())

    app = typer.Typer()

    @app.command()
    def write_atomic_failure(
        config: typer.FileTextWrite = typer.Option(..., atomic=True, lazy=lazy),
    ) -> None:
        config.write("partial-content\n")
        config.flush()
        raise RuntimeError("callback failed")

    result = runner.invoke(app, [f"--config={output_file}"])

    assert result.exit_code == 1
    assert isinstance(result.exception, RuntimeError)
    assert str(result.exception) == "callback failed"
    if destination_exists:
        assert output_file.read_text(encoding="utf-8") == original_content
    else:
        assert not output_file.exists()
    assert set(tmp_path.iterdir()) == initial_entries


@pytest.mark.parametrize(
    ("command_name", "expected_message"),
    [
        ("invalid-atomic-append", "Appending to an existing file is not supported"),
        ("invalid-atomic-exclusive", "Use the `overwrite`-parameter instead."),
        ("invalid-atomic-read", "Atomic writes only make sense with `w`-mode."),
    ],
)
def test_atomic_mode_invalid_options(
    tmp_path: Path, command_name: str, expected_message: str
) -> None:
    output_file = tmp_path / "atomic-invalid-mode.txt"
    output_file.write_text("existing-content\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            command_name,
            f"--config={output_file}",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    assert result.returncode != 0
    combined_output = f"{result.stdout}\n{result.stderr}"
    assert expected_message in combined_output
