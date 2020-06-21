import subprocess


def test_custom_prog_name():
    result = subprocess.run(
        ["python", "prog_name.py", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "custom-name" in result.stdout
