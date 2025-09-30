import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_bytes_type():
    """Test that bytes type works correctly."""
    app = typer.Typer()

    @app.command()
    def main(name: bytes):
        typer.echo(f"Bytes: {name!r}")

    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Bytes: b'hello'" in result.stdout


def test_bytes_option():
    """Test that bytes type works correctly as an option."""
    app = typer.Typer()

    @app.command()
    def main(name: bytes = typer.Option(b"default")):
        typer.echo(f"Bytes: {name!r}")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Bytes: b'default'" in result.stdout

    result = runner.invoke(app, ["--name", "custom"])
    assert result.exit_code == 0
    assert "Bytes: b'custom'" in result.stdout


def test_bytes_argument():
    """Test that bytes type works correctly as an argument."""
    app = typer.Typer()

    @app.command()
    def main(name: bytes = typer.Argument(b"default")):
        typer.echo(f"Bytes: {name!r}")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Bytes: b'default'" in result.stdout

    result = runner.invoke(app, ["custom"])
    assert result.exit_code == 0
    assert "Bytes: b'custom'" in result.stdout


def test_bytes_non_string_input():
    """Test that bytes type works correctly with non-string input."""
    app = typer.Typer()

    @app.command()
    def main(value: bytes):
        typer.echo(f"Bytes: {value!r}")

    # Test with a number (will be converted to string then bytes)
    result = runner.invoke(app, ["123"])
    assert result.exit_code == 0
    assert "Bytes: b'123'" in result.stdout


def test_bytes_conversion_error():
    """Test error handling when bytes conversion fails."""
    import click
    from typer.main import BytesParamType

    bytes_type = BytesParamType()

    # Create a mock object that will raise UnicodeDecodeError when str() is called
    class MockObj:
        def __str__(self):
            # This will trigger the UnicodeDecodeError in the except block
            raise UnicodeDecodeError("utf-8", b"\x80abc", 0, 1, "invalid start byte")

    # Create a mock context for testing
    ctx = click.Context(click.Command("test"))

    # This should raise a click.BadParameter exception
    try:
        bytes_type.convert(MockObj(), None, ctx)
        raise AssertionError(
            "Should have raised click.BadParameter"
        )  # pragma: no cover
    except click.BadParameter:
        pass  # Test passes if we get here
