import pytest
import typer._completion_classes
from typer._completion_classes import _sanitize_help_text


@pytest.mark.parametrize(
    "has_rich, help_text, expected",
    [
        (
            True,
            "help text without rich tags",
            "help text without rich tags",
        ),
        (
            False,
            "help text without rich tags",
            "help text without rich tags",
        ),
        (
            True,
            "help [bold]with[/] rich tags",
            "help with rich tags",
        ),
        (
            False,
            "help [bold]with[/] rich tags",
            "help [bold]with[/] rich tags",
        ),
    ],
)
def test_sanitize_help_text(
    has_rich: bool, help_text: str, expected: str, monkeypatch: pytest.MonkeyPatch
):
    # we can't monkeypatch typer.core.HAS_RICH because _completion_classes will already have imported it before this test runs
    monkeypatch.setattr(typer._completion_classes, "HAS_RICH", has_rich)
    assert _sanitize_help_text(help_text) == expected
