import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_warns_when_callback_is_not_supported():
    app = typer.Typer()

    sub_app = typer.Typer()

    @sub_app.callback()
    def callback():
        """This help text is not used."""

    app.add_typer(sub_app)

    with pytest.warns(
        match="The 'callback' parameter is not supported by Typer when using `add_typer` without a name"
    ):
        try:
            app()
        except SystemExit:
            pass


def test_warns_when_callback_is_not_supported_added_after_add_typer():
    app = typer.Typer()

    sub_app = typer.Typer()
    app.add_typer(sub_app)

    @sub_app.callback()
    def callback():
        """This help text is not used."""

    with pytest.warns(
        match="The 'callback' parameter is not supported by Typer when using `add_typer` without a name"
    ):
        try:
            app()
        except SystemExit:
            pass
