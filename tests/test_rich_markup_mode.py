import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()
rounded = ["╭", "─", "┬", "╮", "│", "├", "┼", "┤", "╰", "┴", "╯"]


def test_rich_markup_mode_default():
    app = typer.Typer()

    @app.command()
    def main(arg: str):
        """Main function"""
        print(f"Hello {arg}")

    assert app.rich_markup_mode is None

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    assert all(c not in result.stdout for c in rounded)


def test_rich_markup_mode_rich():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(arg: str):
        """Main function"""
        print(f"Hello {arg}")

    assert app.rich_markup_mode == "rich"

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    assert any(c in result.stdout for c in rounded)


# Test mostly for coverage
def test_clickexception_rich():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(arg1, arg2: int, arg3: "int", arg4: bool = False, arg5: "bool" = False):
        print(f"arg1: {type(arg1)} {arg1}")
        print(f"arg2: {type(arg2)} {arg2}")
        print(f"arg3: {type(arg3)} {arg3}")
        print(f"arg4: {type(arg4)} {arg4}")
        print(f"arg5: {type(arg5)} {arg5}")

    result = runner.invoke(app, ["Hello", "2", "invalid"])

    assert "Invalid value for 'ARG3': 'invalid' is not a valid integer" in result.stdout
    print(result.stdout)
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )
    print(result.stdout)


# Test mostly for coverage
def test_clickexception_no_rich():
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def main(arg1, arg2: int, arg3: "int", arg4: bool = False, arg5: "bool" = False):
        print(f"arg1: {type(arg1)} {arg1}")
        print(f"arg2: {type(arg2)} {arg2}")
        print(f"arg3: {type(arg3)} {arg3}")
        print(f"arg4: {type(arg4)} {arg4}")
        print(f"arg5: {type(arg5)} {arg5}")

    result = runner.invoke(app, ["Hello", "2", "invalid"])

    assert "Invalid value for 'ARG3': 'invalid' is not a valid integer" in result.stdout
    print(result.stdout)
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )
    print(result.stdout)


# Test mostly for coverage
def test_aborted_rich():
    from docs_src.multiple_values.options_with_multiple_values import tutorial001 as mod

    runner = CliRunner()
    app = typer.Typer(rich_markup_mode="rich")
    app.command()(mod.main)

    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "No user provided" in result.output
    assert "Aborted" in result.output


# Test mostly for coverage
def test_aborted_no_rich():
    from docs_src.multiple_values.options_with_multiple_values import tutorial001 as mod

    runner = CliRunner()
    app = typer.Typer(rich_markup_mode=None)
    app.command()(mod.main)

    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "No user provided" in result.output
    assert "Aborted" in result.output
