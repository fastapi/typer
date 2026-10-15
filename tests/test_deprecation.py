import pytest
import typer
import typer.core
from typer.testing import CliRunner

from tests.utils import needs_rich

runner = CliRunner()


def test_deprecation():
    app = typer.Typer()

    def add_command():
        @app.command()
        def cmd(
            opt: float | None = typer.Option(
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


@pytest.mark.parametrize(
    ("use_rich", "expected"),
    [
        pytest.param(False, "(DEPRECATED)"),
        pytest.param(True, "(deprecated)", marks=needs_rich),
    ],
)
def test_add_typer_keeps_sub_app_deprecated(
    monkeypatch: pytest.MonkeyPatch, use_rich: bool, expected: str
) -> None:
    """A sub-app that marks itself deprecated stays deprecated once added.

    ``add_typer()`` has to leave its own ``deprecated`` default as a
    ``Default()`` placeholder, otherwise it reads as an explicit argument and
    overrides the value the sub-app set on itself.
    """
    monkeypatch.setattr(typer.core, "HAS_RICH", use_rich)

    app = typer.Typer()
    sub_app = typer.Typer(deprecated=True)

    @sub_app.command()
    def sub_command() -> None:
        """Sub command."""  # pragma: no cover

    app.add_typer(sub_app, name="sub")

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert expected in result.output
