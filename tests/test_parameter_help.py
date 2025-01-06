from typing import Annotated

import pytest
import typer
import typer.completion
from typer import Argument, Option
from typer.testing import CliRunner
from typing_extensions import Doc


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize(
    "doc,parameter,expected",
    [
        (Doc("doc only help"), None, "doc only help"),
        (None, Argument(help="argument only help"), "argument only help"),
        (
            Doc("doc help should appear"),
            Argument(),
            "doc help should appear",
        ),
        (
            Doc("this help should not appear"),
            Argument(help="argument help has priority"),
            "argument help has priority",
        ),
        (None, Option(help="option only help"), "option only help"),
        (
            Doc("this help should not appear"),
            Option(help="option help has priority"),
            "option help has priority",
        ),
        (
            Doc("doc help should appear"),
            Option(),
            "doc help should appear",
        ),
    ],
)
def test_doc_help(runner, doc, parameter, expected):
    app = typer.Typer()

    @app.command()
    def main(arg: Annotated[str, doc, parameter]):
        print(f"Hello {arg}")

    result = runner.invoke(app, ["--help"])
    assert expected in result.stdout
