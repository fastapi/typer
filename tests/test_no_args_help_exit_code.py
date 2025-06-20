import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_no_args_is_help_exit_code_zero():
    app = typer.Typer(no_args_is_help=True)

    @app.command()
    def foo():
        """A foo command"""
        print("foo!")

    @app.command()
    def bar():
        """A bar command"""
        print("bar!")

    result = runner.invoke(app, [])
    # It should show help and exit code should be 0
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "foo" in result.output
    assert "bar" in result.output

    # Also check that actual commands still work
    result_foo = runner.invoke(app, ["foo"])
    assert result_foo.exit_code == 0
    assert "foo!" in result_foo.output

    result_bar = runner.invoke(app, ["bar"])
    assert result_bar.exit_code == 0
    assert "bar!" in result_bar.output
