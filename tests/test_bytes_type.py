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


if __name__ == "__main__":
    test_bytes_type()
    test_bytes_option()
    test_bytes_argument()
    print("All tests passed!")
