import sys
from os import getenv

import pytest
from typer.completion import _get_shell_name

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)

needs_linux = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="Test requires Linux"
)

shell_name = _get_shell_name()
needs_bash = pytest.mark.skipif(
    shell_name is None or "bash" not in shell_name, reason="Test requires Bash"
)

requires_completion_permission = pytest.mark.skipif(
    not getenv("_TYPER_RUN_INSTALL_COMPLETION_TESTS", False),
    reason="Test requires permission to run completion installation tests",
)
