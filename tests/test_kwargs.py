import json
from collections.abc import Sequence
from typing import Any

import typer
from typer.testing import CliRunner

runner = CliRunner()


def _args_helper(
    cli_input: Sequence[str],
    expected_args: list[str],
) -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: Any) -> None:
        typer.echo(json.dumps(args))

    result = runner.invoke(app, cli_input)

    assert result.exit_code == 0, "app exited with non-zero status"
    assert expected_args == json.loads(result.output.strip()), (
        "args do not match what is expected"
    )


def _kwargs_helper(
    cli_input: Sequence[str],
    expected_kwargs: dict[str, Any],
) -> None:
    app = typer.Typer()

    @app.command()
    def cmd(**kwargs: Any) -> None:
        typer.echo(json.dumps(kwargs))

    result = runner.invoke(app, cli_input)

    assert result.exit_code == 0, "app exited with non-zero status"
    assert expected_kwargs == json.loads(result.output.strip()), (
        "kwargs do not match what is expected"
    )


def _args_kwargs_helper(
    cli_input: Sequence[str],
    expected_args: list[str],
    expected_kwargs: dict[str, Any],
) -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: Any, **kwargs: Any) -> None:
        typer.echo(json.dumps(args))
        typer.echo(json.dumps(kwargs))

    result = runner.invoke(app, cli_input)

    assert result.exit_code == 0, "app exited with non-zero status"

    json_args, json_kwargs = result.output.splitlines()

    assert expected_args == json.loads(json_args), "args do not match what is expected"
    assert expected_kwargs == json.loads(json_kwargs), (
        "kwargs do not match what is expected"
    )


def _kitchen_sink_helper(
    cli_input: Sequence[str],
    *,
    expected_mandatory: str,
    expected_count: int = 1,
    expected_flag: bool = False,
    expected_args: list[str] | None = None,
    expected_kwargs: dict[str, Any] | None = None,
) -> None:
    app = typer.Typer()

    @app.command()
    def cmd(
        mandatory: str,
        flag: bool = False,
        count: int = 1,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        typer.echo(
            json.dumps(
                {
                    "mandatory": mandatory,
                    "flag": flag,
                    "count": count,
                    "args": list(args),
                    "kwargs": kwargs,
                }
            )
        )

    result = runner.invoke(app, cli_input)

    assert result.exit_code == 0, "app exited with non-zero status"
    assert json.loads(result.output.strip()) == {
        "mandatory": expected_mandatory,
        "flag": expected_flag,
        "count": expected_count,
        "args": expected_args or [],
        "kwargs": expected_kwargs or {},
    }


def test_simple_kwarg() -> None:
    _kwargs_helper(["--flag", "val"], {"flag": "val"})


def test_multiple_kwargs() -> None:
    _kwargs_helper(
        ["--flag", "val", "--flag2", "val2"],
        {"flag": "val", "flag2": "val2"},
    )


def test_kwargs_bool_flag_alone() -> None:
    _kwargs_helper(["--bool-flag"], {"bool_flag": True})


def test_kwargs_two_bool_flags() -> None:
    _kwargs_helper(
        ["--flag1", "--flag2"],
        {"flag1": True, "flag2": True},
    )


def test_kwargs_bool_flags_and_kwargs() -> None:
    _kwargs_helper(
        ["--option1", "value1", "--flag1", "--flag2", "--option2", "value2"],
        {"option1": "value1", "flag1": True, "flag2": True, "option2": "value2"},
    )


def test_args_only_with_separator() -> None:
    _args_helper(["--", "opt1", "opt2"], ["opt1", "opt2"])


def test_args_only_without_separator() -> None:
    _args_helper(["opt1", "opt2"], ["opt1", "opt2"])


def test_no_args_with_separator() -> None:
    _args_helper(["--"], [])


def test_no_args_without_separator() -> None:
    _args_helper([], [])


def test_args_and_kwargs_with_separator() -> None:
    _args_kwargs_helper(
        ["--flag", "val", "--", "opt1", "opt2"],
        ["opt1", "opt2"],
        {"flag": "val"},
    )


def test_args_and_kwargs_without_separator() -> None:
    _args_kwargs_helper(
        ["--flag", "val", "opt1", "opt2"],
        ["opt1", "opt2"],
        {"flag": "val"},
    )


def test_args_kwargs_bool_flag() -> None:
    _args_kwargs_helper(
        ["--flag", "val", "--bool", "--", "opt1", "opt2"],
        ["opt1", "opt2"],
        {"flag": "val", "bool": True},
    )


def test_kwargs_after_separator() -> None:
    _args_kwargs_helper(
        ["--flag", "val", "--", "opt1", "opt2", "--not-a-kwarg", "value"],
        ["opt1", "opt2", "--not-a-kwarg", "value"],
        {"flag": "val"},
    )


def test_double_dash_no_args() -> None:
    _args_kwargs_helper(["--"], [], {})


def test_no_extra_args() -> None:
    _args_kwargs_helper([], [], {})


def test_bool_flag_before_mandatory_arg() -> None:
    _kitchen_sink_helper(
        cli_input=["--unknown-flag", "Alice"],
        expected_mandatory="Alice",
        expected_kwargs={"unknown_flag": True},
    )


def test_known_options_still_work() -> None:
    _kitchen_sink_helper(
        cli_input=["--count", "3", "--extra", "foo", "Alice"],
        expected_mandatory="Alice",
        expected_count=3,
        expected_kwargs={"extra": "foo"},
    )


def test_kwarg_after_known_option() -> None:
    _kitchen_sink_helper(
        cli_input=["--count", "3", "Alice", "--extra", "foo"],
        expected_mandatory="Alice",
        expected_count=3,
        expected_kwargs={"extra": "foo"},
    )


def test_kwarg_and_args_after_known_option() -> None:
    _kitchen_sink_helper(
        cli_input=["--count", "3", "Alice", "--extra", "foo", "other", "args"],
        expected_mandatory="Alice",
        expected_count=3,
        expected_args=["other", "args"],
        expected_kwargs={"extra": "foo"},
    )


def test_kitchen_sink_with_separator() -> None:
    args = ["--flag", "--other-flag", "Alice", "--extra", "foo", "--", "other", "args"]

    _kitchen_sink_helper(
        cli_input=args,
        expected_mandatory="Alice",
        expected_flag=True,
        expected_args=["other", "args"],
        expected_kwargs={"extra": "foo", "other_flag": True},
    )


def test_kitchen_sink_without_separator() -> None:
    args = [
        "--flag1",
        "val",
        "--bool-flag",
        "--count",
        "5",
        "--flag",
        "req1",
        "--",
        "opt1",
        "--not-a",
        "kwarg",
    ]
    _kitchen_sink_helper(
        cli_input=args,
        expected_mandatory="req1",
        expected_flag=True,
        expected_count=5,
        expected_args=["opt1", "--not-a", "kwarg"],
        expected_kwargs={"flag1": "val", "bool_flag": True},
    )
