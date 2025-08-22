import sys
from os import getenv

import pytest

try:
    import shellingham
    from shellingham import ShellDetectionFailure

    shell = shellingham.detect_shell()[0]
except ImportError:  # pragma: no cover
    shellingham = None
    shell = None
except ShellDetectionFailure:  # pragma: no cover
    shell = None


needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)

needs_linux = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="Test requires Linux"
)

needs_bash = pytest.mark.skipif(
    not shellingham or not shell or "bash" not in shell, reason="Test requires Bash"
)

requires_completion_permission = pytest.mark.skipif(
    not getenv("_TYPER_RUN_INSTALL_COMPLETION_TESTS", False),
    reason="Test requires permission to run completion installation tests",
)
