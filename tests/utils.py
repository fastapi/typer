import sys

import pytest

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
