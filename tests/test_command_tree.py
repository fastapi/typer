import subprocess
import sys
from pathlib import Path

import pytest

SUBCOMMANDS = Path(__file__).parent / "assets/subcommand_tree.py"
SUBCMD_FLAG = "--show-sub-commands"
SUBCMD_HELP = "Show sub-command tree"
SUBCMD_TITLE = "Sub-Commands"
SUBCMD_FOOTNOTE = "* denotes "
OVERHEAD_LINES = 3  # footnote plus top/bottom of panel


def prepare_lines(s: str) -> list[str]:
    """
    Takes a string and massages it to a list of modified lines.

    Changes all non-ascii characters to '.', and removes trailing '.' and spaces.
    """
    unified = "".join(
        char if 31 < ord(char) < 127 or char == "\n" else "." for char in s
    ).rstrip()

    # ignore the first 2 characters, and remove
    return [line[2:].rstrip(". ") for line in unified.split("\n")]


def find_in_lines(lines: list[str], cmd: str, help: str) -> bool:
    """
    Looks for a line that starts with 'cmd', and also contains the 'help'.
    """
    for line in lines:
        if line.startswith(cmd) and help in line:
            return True

    return False


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        pytest.param([], True, id="top"),
        pytest.param(["version"], False, id="version"),
        pytest.param(["users"], True, id="users"),
        pytest.param(["users", "add"], False, id="users-add"),
        pytest.param(["users", "delete"], False, id="users-delete"),
        pytest.param(["users", "update"], True, id="users-update"),
        pytest.param(["users", "update", "name"], False, id="users-update-name"),
        pytest.param(["users", "update", "address"], False, id="users-update-address"),
        pytest.param(["pets"], True, id="pets"),
        pytest.param(["pets", "add"], False, id="pets-add"),
        pytest.param(["pets", "list"], False, id="pets-list"),
    ],
)
def test_subcommands_help(args: list[str], expected: bool):
    full_args = (
        [sys.executable, "-m", "coverage", "run", str(SUBCOMMANDS)] + args + ["--help"]
    )
    result = subprocess.run(
        full_args,
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    if expected:
        assert SUBCMD_FLAG in result.stdout
        assert SUBCMD_HELP in result.stdout
    else:
        assert SUBCMD_FLAG not in result.stdout
        assert SUBCMD_HELP not in result.stdout


def test_subcommands_top_tree():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(SUBCOMMANDS), SUBCMD_FLAG],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    lines = prepare_lines(result.stdout)
    expected = [
        ("version*", "Print CLI version and exit"),
        ("users", "Manage users"),
        ("  add*", "Short help"),
        ("  delete*", ""),
        ("  update", "Update user info"),
        ("    name*", "change name"),
        ("    address*", "change address"),
        ("pets", ""),
        ("  add*", "add pet"),
        ("  list*", ""),
    ]
    for command, help in expected:
        assert find_in_lines(lines, command, help), f"Did not find {command} => {help}"
    assert SUBCMD_FOOTNOTE in result.stdout

    assert len(lines) == len(expected) + OVERHEAD_LINES


def test_subcommands_users_tree():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            str(SUBCOMMANDS),
            "users",
            SUBCMD_FLAG,
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    lines = prepare_lines(result.stdout)
    expected = [
        ("add*", "Short help"),
        ("delete*", ""),
        ("update", "Update user info"),
        ("  name*", "change name"),
        ("  address*", "change address"),
    ]
    for command, help in expected:
        assert find_in_lines(lines, command, help), f"Did not find {command} => {help}"
    assert not find_in_lines(lines, "annoy", "Ill advised annoying someone")
    assert SUBCMD_FOOTNOTE in result.stdout

    assert len(lines) == len(expected) + OVERHEAD_LINES


def test_subcommands_users_update_tree():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            str(SUBCOMMANDS),
            "users",
            "update",
            SUBCMD_FLAG,
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    lines = prepare_lines(result.stdout)
    expected = [
        ("name*", "change name"),
        ("address*", "change address"),
    ]
    for command, help in expected:
        assert find_in_lines(lines, command, help), f"Did not find {command} => {help}"
    assert SUBCMD_FOOTNOTE in result.stdout

    assert len(lines) == len(expected) + OVERHEAD_LINES


@pytest.mark.parametrize(
    ["args", "message"],
    [
        pytest.param(["version"], "My CLI Version 1.0", id="version"),
        pytest.param(
            ["users", "add", "John Doe", "--address", "55 Main St"],
            "Adding user: John Doe at 55 Main St",
            id="users-add",
        ),
        pytest.param(
            ["users", "delete", "Bob Smith"],
            "Deleting user: Bob Smith",
            id="users-delete",
        ),
        pytest.param(
            ["users", "annoy", "Bill"],
            "Annoying Bill",
            id="users-annoy",
        ),
        pytest.param(
            ["users", "update", "name", "Jane Smith", "Bob Doe"],
            "Updating user: Jane Smith => Bob Doe",
            id="users-update-name",
        ),
        pytest.param(
            ["users", "update", "address", "Bob Doe", "Drury Lane"],
            "Updating user Bob Doe address: Drury Lane",
            id="users-update-address",
        ),
        pytest.param(
            ["pets", "add", "Fluffy"], "Adding pet named Fluffy", id="pets-add"
        ),
        pytest.param(["pets", "list"], "Need to compile list of pets", id="pets-list"),
    ],
)
def test_subcommands_execute(args: list[str], message: str):
    full_args = [sys.executable, "-m", "coverage", "run", str(SUBCOMMANDS)] + args
    result = subprocess.run(
        full_args,
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert message in result.stdout
