import sys

import pytest


needs_py38 = pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8+")


needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)

needs_linux = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="Test requires Linux"
)
