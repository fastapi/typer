import os
import sys

import pytest

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)

needs_bash = pytest.mark.skipif(
    "bash" not in os.environ.get("SHELL", ""), reason="Test requires Bash"
)
