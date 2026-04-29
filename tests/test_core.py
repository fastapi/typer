from typing import Annotated

import pytest
import typer
import typer._completion_shared
import typer.completion
from typer import _click
from typer.core import TyperArgument, TyperCommand, TyperGroup, TyperOption, _split_opt
from typer.testing import CliRunner

runner = CliRunner()


def test_human_readable_name() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        my_arg_1: Annotated[str, typer.Argument()],
        my_arg_2: Annotated[str, typer.Argument(metavar="META_ARG")],
        my_opt: Annotated[str, typer.Option()],
    ):
        pass  # pragma: no cover

    command = typer.main.get_command(app)
    params = {param.name: param for param in command.params}

    assert params["my_arg_1"].human_readable_name == "MY_ARG_1"
    assert params["my_arg_2"].human_readable_name == "META_ARG"
    assert params["my_opt"].human_readable_name == "my_opt"


def test_parameter_metavar() -> None:
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def cmd(name: Annotated[str, typer.Option(metavar="CUSTOM")]) -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--name CUSTOM" in result.output


def test_parameter_nargs_gt_1() -> None:
    param = TyperArgument(param_decls=["value"], type=str, nargs=2)
    ctx = _click.Context(TyperCommand(name="cmd"))

    assert param.type_cast_value(ctx, ("one", "two")) == ("one", "two")

    with pytest.raises(
        _click.exceptions.BadParameter, match="Takes 2 values but 1 given."
    ):
        param.type_cast_value(ctx, ("one",))


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
    ("envvar", "auto_prefix", "set_env", "expected"),
    [
        ("APP_NAME", None, True, "my-precious"),
        (None, "APP", True, "my-precious"),
        (None, None, False, None),
    ],
)
def test_option_resolve_envvar(
    monkeypatch: pytest.MonkeyPatch,
    envvar: str | None,
    auto_prefix: str | None,
    set_env: bool,
    expected: str | None,
) -> None:
    option = TyperOption(
        param_decls=["name", "--name"],
        required=False,
        envvar=envvar,
    )
    if set_env:
        monkeypatch.setenv("APP_NAME", "my-precious")

    ctx = _click.Context(TyperCommand(name="cmd"), auto_envvar_prefix=auto_prefix)
    assert option.resolve_envvar_value(ctx) == expected


def test_option_resolve_envvar_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    option = TyperOption(
        param_decls=["name", "--name"],
        required=False,
        envvar=["APP_NAME_1", "APP_NAME_2"],
    )
    monkeypatch.delenv("APP_NAME_1", raising=False)
    monkeypatch.delenv("APP_NAME_2", raising=False)
    ctx = _click.Context(TyperCommand(name="cmd"))

    assert option.resolve_envvar_value(ctx) is None


def test_context_auto_envvar() -> None:
    app = typer.Typer(context_settings={"auto_envvar_prefix": "APP"})
    sub_app = typer.Typer()

    @sub_app.command()
    def clone(ctx: typer.Context) -> None:
        print(ctx.auto_envvar_prefix)

    app.add_typer(sub_app, name="beth")

    result = runner.invoke(app, ["beth", "clone"])
    assert result.exit_code == 0
    assert "APP_BETH_CLONE" in result.stdout


def test_context_with_resource() -> None:
    events: list[str] = []

    class DemoResource:
        def __enter__(self) -> str:
            events.append("enter")
            return "pickle-rick"

        def __exit__(self, *args: object) -> None:
            events.append("exit")

    app = typer.Typer()

    @app.command()
    def cmd(ctx: typer.Context) -> None:
        value = ctx.with_resource(DemoResource())
        assert value == "pickle-rick"
        assert events == ["enter"]
        print("I'm a pickle")

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "I'm a pickle" in result.stdout
    assert events == ["enter", "exit"]


def test_context_find_root() -> None:
    app = typer.Typer()
    sub_app = typer.Typer()

    @sub_app.command()
    def child(ctx: typer.Context) -> None:
        root = ctx.find_root()
        assert root.parent is None
        assert root is ctx.parent.parent
        print("ok")

    app.add_typer(sub_app, name="sub")

    result = runner.invoke(app, ["sub", "child"])
    assert result.exit_code == 0
    assert "ok" in result.stdout


def test_context_find_object() -> None:
    class Marker:
        pass

    marker = Marker()
    app = typer.Typer()

    @app.callback()
    def callback(ctx: typer.Context) -> None:
        ctx.obj = marker

    @app.command()
    def child(ctx: typer.Context) -> None:
        assert ctx.find_object(Marker) is marker
        assert ctx.find_object(str) is None
        print("ok")

    result = runner.invoke(app, ["child"])
    assert result.exit_code == 0
    assert "ok" in result.stdout


def test_context_lookup_default_callable() -> None:
    app = typer.Typer()

    @app.command()
    def child(ctx: typer.Context) -> None:
        ctx.default_map = {"planet": lambda: "Earth"}
        assert ctx.lookup_default("planet") == "Earth"
        value = ctx.lookup_default("planet", call=False)
        assert callable(value)
        print("ok")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "ok" in result.stdout


def test_context_abort() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(ctx: typer.Context) -> None:
        ctx.abort()

    result = runner.invoke(app, standalone_mode=False)
    assert result.exit_code == 1
    assert isinstance(result.exception, _click.core.Abort)


def test_command_help_disabled() -> None:
    app = typer.Typer()

    @app.command(add_help_option=False)
    def cmd() -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"], standalone_mode=False)
    assert result.exit_code == 1
    assert isinstance(result.exception, _click.exceptions.NoSuchOption)
    assert result.exception.option_name == "--help"


def test_command_help_deprecated() -> None:
    app = typer.Typer(rich_markup_mode=None, epilog="Built with love")

    @app.command(short_help="Shorty", help="Regular help text.", deprecated=True)
    def one() -> None:
        pass  # pragma: no cover

    @app.command()
    def two() -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["one", "--help"])
    assert result.exit_code == 0
    assert "Regular help text. (DEPRECATED)" in result.output

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Built with love" in result.output
    assert "oneShorty(DEPRECATED)" in result.output.replace(" ", "")


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
