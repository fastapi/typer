from typing import Annotated

import pytest
import typer
import typer._completion_shared
import typer.completion
from typer import _click
from typer.core import TyperCommand, TyperGroup, _split_opt
from typer.testing import CliRunner

runner = CliRunner()


def test_parameter_metavar() -> None:
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def cmd(name: Annotated[str, typer.Option(metavar="CUSTOM")]) -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--name CUSTOM" in result.output


def test_tuple_argument_wrong_arity() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(value: tuple[str, str]):
        pass  # pragma: no cover

    result = runner.invoke(app, ["only-one"])
    assert result.exit_code == 2
    assert "takes 2 values" in result.output


def test_count_option() -> None:
    app = typer.Typer()

    @app.command()
    def main(verbose: int = typer.Option(0, "--verbose", "-v", count=True)):
        print(verbose)

    result = runner.invoke(app, ["-vvv"])
    assert result.exit_code == 0
    assert "3" in result.stdout


def test_duplicate_declaration_raises() -> None:
    app = typer.Typer()

    @app.command()
    def main(name: str = typer.Option(..., "name", "name")):
        pass  # pragma: no cover

    with pytest.raises(TypeError, match="Name 'name' defined twice"):
        typer.main.get_command(app)


def test_invalid_boolean_flag_declaration_raises() -> None:
    app = typer.Typer()

    @app.command()
    def main(flag: bool = typer.Option(False, "--flag/--flag")):
        pass  # pragma: no cover

    with pytest.raises(ValueError, match="cannot use the same flag for true/false"):
        typer.main.get_command(app)


def test_option_error_hint() -> None:
    app = typer.Typer()

    @app.command()
    def main(age: int = typer.Option(..., envvar="APP_NAME", show_envvar=True)):
        pass  # pragma: no cover

    result = runner.invoke(app, ["--age", "not-int"])
    assert result.exit_code == 2
    assert "(env var: 'APP_NAME')" in result.output


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
    context_settings = {"auto_envvar_prefix": auto_prefix} if auto_prefix else {}
    app = typer.Typer(context_settings=context_settings)

    @app.command()
    def main(name: str = typer.Option("fallback", envvar=envvar)):
        print(name)

    if set_env:
        monkeypatch.setenv("APP_NAME", "my-precious")

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    if expected is None:
        assert "fallback" in result.stdout
    else:
        assert expected in result.stdout


def test_option_resolve_envvar_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = typer.Typer()

    @app.command()
    def main(
        name: str = typer.Option("fallback", envvar=["APP_NAME_1", "APP_NAME_2"]),
    ):
        print(name)

    monkeypatch.delenv("APP_NAME_1", raising=False)
    monkeypatch.delenv("APP_NAME_2", raising=False)

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "fallback" in result.stdout


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


def test_nargs_default_map():
    app = typer.Typer()

    @app.command()
    def main(names: list[str] = typer.Option(None)):
        print(names)  # pragma: no cover

    result = runner.invoke(app, [], default_map={"names": "not-a-list"})
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_parameter_name_casing():
    app = typer.Typer()

    @app.command()
    def main(
        arg1: int,
        arg2: int = 42,
        arg3: int = typer.Argument(...),
        ARG4: int = typer.Argument(42),
        ARG5: int = typer.Option(...),
        arg6: int = typer.Option(42),
        arg7: int = typer.Argument(42, metavar="meta7"),
        arg8: int = typer.Argument(metavar="ARG8"),
        arg9: int = typer.Option(metavar="ARG9"),
    ):
        print(
            f"arg1={arg1} arg2={arg2} arg3={arg3} ARG4={ARG4} ARG5={ARG5} "
            f"arg6={arg6} arg7={arg7} arg8={arg8} arg9={arg9}"
        )

    result = runner.invoke(
        app,
        [
            "1",
            "3",
            "4",
            "7",
            "8",
            "--arg2",
            "2",
            "--ARG5",
            "5",
            "--arg6",
            "6",
            "--ARG9",
            "9",
        ],
    )
    assert result.exit_code == 0
    assert (
        "arg1=1 arg2=2 arg3=3 ARG4=4 ARG5=5 arg6=6 arg7=7 arg8=8 arg9=9"
        in result.output
    )

    result = runner.invoke(app, ["1", "3", "4", "7", "8", "--ARG5", "5", "--ARG9", "9"])
    assert result.exit_code == 0
    assert (
        "arg1=1 arg2=42 arg3=3 ARG4=4 ARG5=5 arg6=42 arg7=7 arg8=8 arg9=9"
        in result.output
    )

    result = runner.invoke(app, ["1", "3", "4", "7", "8", "--arg5", "5", "--ARG9", "9"])
    assert result.exit_code != 0
    assert "No such option: --arg5" in result.output

    result = runner.invoke(app, ["1", "3", "4", "7", "8", "--ARG5", "5", "--arg9", "9"])
    assert result.exit_code != 0
    assert "No such option: --arg9" in result.output
