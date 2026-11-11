import shutil
import subprocess
from unittest import mock

import pytest
from typer import _click
from typer._completion_classes import BashComplete


def _check_version_with(bash_version: str) -> bool:
    """Run BashComplete._check_version against a faked Bash and report
    whether it warned that completion is unsupported.
    """
    completed = subprocess.CompletedProcess(
        args=["bash", "--norc", "-c", 'echo "${BASH_VERSION}"'],
        returncode=0,
        stdout=f"{bash_version}\n".encode(),
    )
    with (
        mock.patch.object(shutil, "which", return_value="/usr/bin/bash"),
        mock.patch.object(subprocess, "run", return_value=completed),
        mock.patch.object(_click.utils, "echo") as echo,
    ):
        BashComplete._check_version()
    return echo.called


@pytest.mark.parametrize(
    "bash_version",
    ["3.2.57", "4.0.0", "4.3.9", "4.3.99"],
)
def test_bash_too_old_is_reported_unsupported(bash_version: str):
    assert _check_version_with(bash_version) is True


@pytest.mark.parametrize(
    "bash_version",
    ["4.4.0", "4.5.0", "4.9.0", "5.0.0", "5.3.0"],
)
def test_bash_new_enough_is_supported(bash_version: str):
    assert _check_version_with(bash_version) is False


@pytest.mark.parametrize(
    "bash_version",
    ["4.10.0", "4.11.2", "5.10.0", "10.0.0", "12.3.4"],
)
def test_bash_two_digit_version_components_are_supported(bash_version: str):
    """Version components must be compared numerically.

    "10" sorts before "4" as a string, so a lexicographic comparison wrongly
    reports these versions as older than 4.4.
    """
    assert _check_version_with(bash_version) is False
