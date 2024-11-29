from typing import Optional

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_deprecation():
    app = typer.Typer()

    def add_command():
        @app.command()
        def cmd(
            opt: Optional[float] = typer.Option(
                3.14,
                is_flag=True,
                flag_value="42",
                help="Some wonderful number",
            ),
        ): ...  # pragma: no cover

    with pytest.warns(
        match="The 'is_flag' and 'flag_value' parameters are not supported by Typer"
    ):
        add_command()
