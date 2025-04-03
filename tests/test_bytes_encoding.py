import typer
import base64
import binascii
from typer.testing import CliRunner

runner = CliRunner()


def test_base64_encode_decode():
    """Test base64 encoding and decoding with bytes type."""
    app = typer.Typer()

    @app.command()
    def encode(text: bytes):
        """Encode text to base64."""
        encoded = base64.b64encode(text)
        typer.echo(encoded.decode())

    @app.command()
    def decode(encoded: str):
        """Decode base64 to bytes."""
        decoded = base64.b64decode(encoded)
        typer.echo(repr(decoded))

    # Test encoding
    result = runner.invoke(app, ["encode", "Hello, world!"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "SGVsbG8sIHdvcmxkIQ=="

    # Test decoding
    result = runner.invoke(app, ["decode", "SGVsbG8sIHdvcmxkIQ=="])
    assert result.exit_code == 0
    assert result.stdout.strip() == repr(b'Hello, world!')


def test_hex_encode_decode():
    """Test hex encoding and decoding with bytes type."""
    app = typer.Typer()

    @app.command()
    def to_hex(data: bytes):
        """Convert bytes to hex string."""
        hex_str = binascii.hexlify(data).decode()
        typer.echo(hex_str)

    @app.command()
    def from_hex(hex_str: str):
        """Convert hex string to bytes."""
        data = binascii.unhexlify(hex_str)
        typer.echo(repr(data))

    # Test to_hex
    result = runner.invoke(app, ["to-hex", "ABC123"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "414243313233"  # Hex for "ABC123"

    # Test from_hex
    result = runner.invoke(app, ["from-hex", "414243313233"])
    assert result.exit_code == 0
    assert result.stdout.strip() == repr(b'ABC123')


def test_complex_bytes_operations():
    """Test more complex operations with bytes type."""
    app = typer.Typer()

    @app.command()
    def main(
        data: bytes = typer.Argument(..., help="Data to process"),
        encoding: str = typer.Option("utf-8", help="Encoding to use for output"),
        prefix: bytes = typer.Option(b"PREFIX:", help="Prefix to add to the data"),
    ):
        """Process bytes data with options."""
        result = prefix + data
        typer.echo(result.decode(encoding))

    # Test with default encoding
    result = runner.invoke(app, ["Hello"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "PREFIX:Hello"

    # Test with custom encoding
    result = runner.invoke(app, ["Hello", "--encoding", "ascii"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "PREFIX:Hello"

    # Test with custom prefix
    result = runner.invoke(app, ["Hello", "--prefix", "CUSTOM:"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "CUSTOM:Hello"


if __name__ == "__main__":
    test_base64_encode_decode()
    test_hex_encode_decode()
    test_complex_bytes_operations()
    print("All tests passed!")
