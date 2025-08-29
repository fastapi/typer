from importlib.machinery import ModuleSpec
from typing import Union
from unittest.mock import patch

import pytest
from typer._completion_classes import _sanitize_help_text


@pytest.mark.parametrize(
    "find_spec, help_text, expected",
    [
        (
            ModuleSpec("rich", loader=None),
            "help text without rich tags",
            "help text without rich tags",
        ),
        (
            None,
            "help text without rich tags",
            "help text without rich tags",
        ),
        (
            ModuleSpec("rich", loader=None),
            "help [bold]with[/] rich tags",
            "help with rich tags",
        ),
        (
            None,
            "help [bold]with[/] rich tags",
            "help [bold]with[/] rich tags",
        ),
    ],
)
def test_sanitize_help_text(
    find_spec: Union[ModuleSpec, None], help_text: str, expected: str
):
    with patch("importlib.util.find_spec", return_value=find_spec) as mock_find_spec:
        assert _sanitize_help_text(help_text) == expected
    mock_find_spec.assert_called_once_with("rich")
