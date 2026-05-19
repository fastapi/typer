import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import typer
from typer.testing import CliRunner

runner = CliRunner()


def _kitchen_sink_helper(
    cli_input: Sequence[str],
    *,
    expected_filepath: str,
    expected_option: str = "",
    expected_flag: bool = False,
    expected_args: list[str] | None = None,
    expected_kwargs: dict[str, Any] | None = None,
) -> None:
    app = typer.Typer()

    @app.command()
    def cmd(
        filepath: Path,
        option: str = "",
        flag: bool = False,
        *args: str,
        **kwargs: Any,
    ) -> None:
        typer.echo(
            json.dumps(
                {
                    "filepath": str(filepath),
                    "option": option,
                    "flag": flag,
                    "args": list(args),
                    "kwargs": kwargs,
                }
            )
        )

    result = runner.invoke(app, cli_input)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output.strip()) == {
        "filepath": expected_filepath,
        "option": expected_option,
        "flag": expected_flag,
        "args": expected_args or [],
        "kwargs": expected_kwargs or {},
    }


def _separate_args_kwargs_helper(
    cli_input: Sequence[str],
    *,
    expected_filepath: str,
    expected_args: list[str] | None = None,
    expected_kwargs: dict[str, Any] | None = None,
) -> None:
    app = typer.Typer()

    @app.command()
    def args(filepath: Path, *args: str) -> None:
        typer.echo(json.dumps({"filepath": str(filepath), "args": list(args)}))

    @app.command()
    def kwargs(filepath: Path, **kwargs: Any) -> None:
        typer.echo(json.dumps({"filepath": str(filepath), "kwargs": kwargs}))

    result = runner.invoke(app, cli_input)
    assert result.exit_code == 0, result.output

    data = json.loads(result.output.strip())
    assert data["filepath"] == expected_filepath
    if expected_args is not None:
        assert data["args"] == expected_args
    if expected_kwargs is not None:
        assert data["kwargs"] == expected_kwargs


def test_unknown_kwarg_and_trailing_args() -> None:
    _kitchen_sink_helper(
        ["--unknown-key", "value", "input.txt", "arg1", "arg2"],
        expected_filepath="input.txt",
        expected_kwargs={"unknown_key": "value"},
        expected_args=["arg1", "arg2"],
    )


def test_known_flag() -> None:
    _kitchen_sink_helper(
        ["input.txt", "--flag"],
        expected_filepath="input.txt",
        expected_flag=True,
    )


def test_separator_absorbs_flag() -> None:
    _kitchen_sink_helper(
        ["input.txt", "--", "--flag"],
        expected_filepath="input.txt",
        expected_args=["--flag"],
    )


def test_equivalent_form_1() -> None:
    _kitchen_sink_helper(
        ["--option", "val", "--flag", "input.txt", "arg1", "arg2", "--unknown", "val2"],
        expected_filepath="input.txt",
        expected_option="val",
        expected_flag=True,
        expected_args=["arg1", "arg2"],
        expected_kwargs={"unknown": "val2"},
    )


def test_equivalent_form_2() -> None:
    _kitchen_sink_helper(
        ["input.txt", "--option", "val", "--flag", "arg1", "arg2", "--unknown", "val2"],
        expected_filepath="input.txt",
        expected_option="val",
        expected_flag=True,
        expected_args=["arg1", "arg2"],
        expected_kwargs={"unknown": "val2"},
    )


def test_equivalent_form_3() -> None:
    _kitchen_sink_helper(
        ["--unknown", "val2", "input.txt", "--option", "val", "--flag", "arg1", "arg2"],
        expected_filepath="input.txt",
        expected_option="val",
        expected_flag=True,
        expected_args=["arg1", "arg2"],
        expected_kwargs={"unknown": "val2"},
    )


def test_equivalent_form_4() -> None:
    _kitchen_sink_helper(
        ["--flag", "--option", "val", "--unknown", "val2", "input.txt", "arg1", "arg2"],
        expected_filepath="input.txt",
        expected_option="val",
        expected_flag=True,
        expected_args=["arg1", "arg2"],
        expected_kwargs={"unknown": "val2"},
    )


def test_unknown_flag_requires_value() -> None:
    _kitchen_sink_helper(
        ["--unknown-flag", "true", "input.txt", "arg1", "arg2"],
        expected_filepath="input.txt",
        expected_kwargs={"unknown_flag": "true"},
        expected_args=["arg1", "arg2"],
    )


def test_command2_args() -> None:
    _separate_args_kwargs_helper(
        ["args", "input.txt", "arg1", "arg2"],
        expected_filepath="input.txt",
        expected_args=["arg1", "arg2"],
    )


def test_command2_kwargs() -> None:
    _separate_args_kwargs_helper(
        ["kwargs", "input.txt", "--key", "value"],
        expected_filepath="input.txt",
        expected_kwargs={"key": "value"},
    )


def test_unknown_option_without_value_errors() -> None:
    """Unknown option with no value is left in remaining so Click emits an error.

    Covers core.py _extract_unknown_options else-branch (lines 676-677).
    """
    app = typer.Typer()

    @app.command()
    def cmd(**kwargs: Any) -> None:
        typer.echo(json.dumps(kwargs))

    result = runner.invoke(app, ["--unknown-flag"])
    assert result.exit_code != 0


def test_keyword_only_param_after_args() -> None:
    """Named option declared after *args (keyword-only) is passed correctly.

    Covers main.py _kw_only_names branch (lines 1552-1553).
    """
    app = typer.Typer()

    @app.command()
    def cmd(*args: str, option: str = "default") -> None:
        typer.echo(json.dumps({"args": list(args), "option": option}))

    result = runner.invoke(app, ["--option", "custom", "a", "b"])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output.strip()) == {"args": ["a", "b"], "option": "custom"}


def test_empty_args_without_separator() -> None:
    """./command.py input.txt  →  args = ()"""
    _kitchen_sink_helper(
        ["input.txt"],
        expected_filepath="input.txt",
        expected_args=[],
    )


def test_empty_args_with_separator() -> None:
    """./command.py input.txt --  →  args = ()"""
    _kitchen_sink_helper(
        ["input.txt", "--"],
        expected_filepath="input.txt",
        expected_args=[],
    )
