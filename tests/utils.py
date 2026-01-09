import re
import sys
from os import getenv

import pytest
from typer._completion_shared import _get_shell_name

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)

needs_linux = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="Test requires Linux"
)

shell = _get_shell_name()
needs_bash = pytest.mark.skipif(
    shell is None or "bash" not in shell, reason="Test requires Bash"
)

requires_completion_permission = pytest.mark.skipif(
    not getenv("_TYPER_RUN_INSTALL_COMPLETION_TESTS", False),
    reason="Test requires permission to run completion installation tests",
)


def strip_double_spaces(text: str) -> str:
    return re.sub(r" {2,}", " ", text)


def normalize_rich_output(
    text: str, replace_with: str = "*", squash_whitespaces: bool = True
) -> str:
    """
    Replace all rich formatting characters with a simple placeholder.
    """
    text = re.sub(r"\x1b\[[0-9;]*m", replace_with, text)
    text = re.sub(r"[\u2500-\u257F]", replace_with, text)
    text = re.sub(r"[\U0001F300-\U0001F6FF]", replace_with, text)
    text = re.sub(f"{re.escape(replace_with)}+", replace_with, text)
    if squash_whitespaces:
        text = strip_double_spaces(text)
    return text
