import os
import subprocess
import sys


def run_with_seed(asset: str, seed: int, *args: str) -> str:
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "-m", "typer", asset, "run", *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout


def test_first_app_in_file_is_used_for_any_seed():
    outputs = {
        run_with_seed("tests/assets/cli/multi_app_any_name.py", seed)
        for seed in range(8)
    }
    assert outputs == {"zeta\n"}


def test_first_function_in_file_is_used_not_an_import():
    outputs = {
        run_with_seed(
            "tests/assets/cli/func_other_name_with_import.py", seed, "--name", "Camila"
        )
        for seed in range(8)
    }
    assert len(outputs) == 1
    assert "Hello Camila" in outputs.pop()
