import subprocess
import sys
from textwrap import dedent

import pytest


@pytest.mark.skipif(sys.version_info < (3, 15), reason="PEP 810 requires Python 3.15")
def test_public_command_class_is_loaded_on_first_use():
    subprocess.run(
        [
            sys.executable,
            "-X",
            "lazy_imports=normal",
            "-c",
            dedent(
                """\
                import sys
                import typer

                assert "typer.main" not in sys.modules
                app = typer.Typer()
                assert type(app) is sys.modules["typer.main"].Typer
                """
            ),
        ],
        check=True,
    )
