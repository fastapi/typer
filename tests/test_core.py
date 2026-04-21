from typing import Annotated

import pytest
import typer
import typer._completion_shared
import typer.completion
from typer import _click
from typer.core import TyperArgument, TyperCommand, TyperGroup, TyperOption, _split_opt
from typer.testing import CliRunner

runner = CliRunner()


def test_argument_name() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        name: str,
        target: Annotated[str, typer.Argument(metavar="META_TARGET")],
    ):
        pass  # pragma: no cover

    command = typer.main.get_command(app)
    params = {param.name: param for param in command.params}

    assert params["name"].human_readable_name == "NAME"
    assert params["target"].human_readable_name == "META_TARGET"


def test_parameter_constructor() -> None:
    # no param_decl and expose_value is False: sets name to None
    arg = TyperArgument(param_decls=[], expose_value=False)
    assert arg.name is None
    assert arg.opts == []
    assert arg.secondary_opts == []

    # no param_decl and expose_value is True: raises
    with pytest.raises(TypeError, match="does not have a name."):
        TyperArgument(param_decls=[], expose_value=True)

    # len(param_decl) > 1: raises
    with pytest.raises(TypeError, match="take exactly one parameter declaration"):
        TyperArgument(param_decls=["first", "second"])

    # duplicated identifier in option declarations: raises
    with pytest.raises(TypeError, match="Name 'name' defined twice"):
        TyperOption(param_decls=["name", "name"], required=False)

    # same true/false flag in boolean option declaration: raises
    with pytest.raises(ValueError, match="cannot use the same flag for true/false"):
        TyperOption(param_decls=["flag", "--flag/--flag"], required=False, is_flag=True)

    # inferred name is not a valid identifier: sets name to None
    unnamed_option = TyperOption(param_decls=["--123"], required=False)
    assert unnamed_option.name is None

    # no param_decl and prompt=True: raises
    with pytest.raises(TypeError, match="'name' is required with 'prompt=True'."):
        TyperOption(param_decls=[], expose_value=False, prompt=True, required=False)

    # count works
    option = TyperOption(
        param_decls=["verbose", "--verbose", "-v"],
        type=None,
        default=0,
        required=False,
        count=True,
    )
    assert isinstance(option.type, _click.types.IntRange)
    assert option.type.min == 0


def test_option_error_hint() -> None:
    option = TyperOption(
        param_decls=["name", "--name"],
        required=False,
        show_envvar=True,
        envvar="APP_NAME",
    )
    hint = option.get_error_hint(_click.Context(TyperCommand(name="cmd")))
    assert "(env var: 'APP_NAME')" in hint


def test_group_init() -> None:
    group_no_commands = TyperGroup(name="root", commands=None)
    assert group_no_commands.commands == {}

    named = TyperCommand(name="named")
    unnamed = TyperCommand(name=None)
    group_command_sequence = TyperGroup(name="root", commands=[named, unnamed])
    assert group_command_sequence.commands == {"named": named}


@pytest.mark.parametrize("with_result_callback", [False, True])
def test_group_result_callback(with_result_callback: bool) -> None:
    called = {"child": False, "result_callback": False}

    def child_callback() -> None:
        called["child"] = True
        return None

    def result_callback(value, **kwargs):  # type: ignore[no-untyped-def]
        called["result_callback"] = True
        return value

    child = TyperCommand(name="child", callback=child_callback)
    group = TyperGroup(
        name="root",
        commands={"child": child},
        result_callback=result_callback if with_result_callback else None,
    )
    ctx = group.make_context("root", ["child"])

    result = group.invoke(ctx)

    assert result is None
    assert called["child"] is True
    assert called["result_callback"] is with_result_callback
    assert ctx.invoked_subcommand == "child"


def test_group_add_command() -> None:
    group = TyperGroup(name="root")
    unnamed_command = TyperCommand(name=None)

    with pytest.raises(TypeError, match="Command has no name."):
        group.add_command(unnamed_command)


def test_group_click_resolve_command() -> None:
    child = TyperCommand(name="child")
    group = TyperGroup(name="root", commands={"child": child})
    ctx = group.make_context("root", ["CHILD"], token_normalize_func=str.lower)

    cmd_name, cmd, remaining = group._click_resolve_command(ctx, ["CHILD"])

    assert cmd_name == "child"
    assert cmd is child
    assert remaining == []


@pytest.mark.parametrize(
    ("envvar", "auto_prefix"),
    [
        ("APP_NAME", None),
        (None, "APP"),
    ],
)
def test_option_resolve_envvar(
    monkeypatch: pytest.MonkeyPatch,
    envvar: str | None,
    auto_prefix: str | None,
) -> None:
    option = TyperOption(
        param_decls=["name", "--name"],
        required=False,
        envvar=envvar,
    )
    monkeypatch.setenv("APP_NAME", "my-precious")

    ctx = _click.Context(TyperCommand(name="cmd"), auto_envvar_prefix=auto_prefix)
    assert option.resolve_envvar_value(ctx) == "my-precious"


@pytest.mark.parametrize(
    ("value", "expected_prefix", "expected_opt"),
    [
        ("--verbose", "--", "verbose"),
        ("//verbose", "//", "verbose"),
        ("-verbose", "-", "verbose"),
        ("verbose", "", "verbose"),
    ],
)
def test_split_opt(value: str, expected_prefix: str, expected_opt: str) -> None:
    prefix, opt = _split_opt(value)
    assert prefix == expected_prefix
    assert opt == expected_opt
