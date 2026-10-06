import base64
import binascii

import typer

app = typer.Typer()


@app.command()
def base64_encode(text: bytes):
    """Encode text to base64."""
    encoded = base64.b64encode(text)
    typer.echo(f"Original: {text!r}")
    typer.echo(f"Base64 encoded: {encoded.decode()}")


@app.command()
def base64_decode(encoded: str):
    """Decode base64 to bytes."""
    try:
        decoded = base64.b64decode(encoded)
        typer.echo(f"Base64 encoded: {encoded}")
        typer.echo(f"Decoded: {decoded!r}")
        typer.echo(f"As string: {decoded.decode(errors='replace')}")
    except Exception as e:
        typer.echo(f"Error decoding base64: {e}", err=True)
        raise typer.Exit(code=1) from e


@app.command()
def hex_encode(data: bytes):
    """Convert bytes to hex string."""
    hex_str = binascii.hexlify(data).decode()
    typer.echo(f"Original: {data!r}")
    typer.echo(f"Hex encoded: {hex_str}")


@app.command()
def hex_decode(hex_str: str):
    """Convert hex string to bytes."""
    try:
        data = binascii.unhexlify(hex_str)
        typer.echo(f"Hex encoded: {hex_str}")
        typer.echo(f"Decoded: {data!r}")
        typer.echo(f"As string: {data.decode(errors='replace')}")
    except Exception as e:
        typer.echo(f"Error decoding hex: {e}", err=True)
        raise typer.Exit(code=1) from e


@app.command()
def convert(
    data: bytes = typer.Argument(..., help="Data to convert"),
    from_format: str = typer.Option(
        "raw", "--from", "-f", help="Source format: raw, base64, or hex"
    ),
    to_format: str = typer.Option(
        "base64", "--to", "-t", help="Target format: raw, base64, or hex"
    ),
):
    """Convert between different encodings."""
    # First decode from source format to raw bytes
    raw_bytes = data
    if from_format == "base64":
        try:
            raw_bytes = base64.b64decode(data)
        except Exception as e:
            typer.echo(f"Error decoding base64: {e}", err=True)
            raise typer.Exit(code=1) from e
    elif from_format == "hex":
        try:
            raw_bytes = binascii.unhexlify(data)
        except Exception as e:
            typer.echo(f"Error decoding hex: {e}", err=True)
            raise typer.Exit(code=1) from e
    elif from_format != "raw":
        typer.echo(f"Unknown source format: {from_format}", err=True)
        raise typer.Exit(code=1)

    # Then encode to target format
    if to_format == "raw":
        typer.echo(f"Raw bytes: {raw_bytes!r}")
        typer.echo(f"As string: {raw_bytes.decode(errors='replace')}")
    elif to_format == "base64":
        encoded = base64.b64encode(raw_bytes).decode()
        typer.echo(f"Base64 encoded: {encoded}")
    elif to_format == "hex":
        encoded = binascii.hexlify(raw_bytes).decode()
        typer.echo(f"Hex encoded: {encoded}")
    else:
        typer.echo(f"Unknown target format: {to_format}", err=True)
        raise typer.Exit(code=1)


@app.command()
def convert_latin1(
    data: bytes = typer.Argument(
        ..., help="Data to convert (latin-1)", encoding="latin-1"
    ),
    from_format: str = typer.Option(
        "raw", "--from", "-f", help="Source format: raw, base64, or hex"
    ),
    to_format: str = typer.Option(
        "base64", "--to", "-t", help="Target format: raw, base64, or hex"
    ),
):
    """Convert using latin-1 input decoding for the bytes argument."""
    # Reuse the same logic as convert()
    raw_bytes = data
    if from_format == "base64":
        try:
            raw_bytes = base64.b64decode(data)
        except Exception as e:
            typer.echo(f"Error decoding base64: {e}", err=True)
            raise typer.Exit(code=1) from e
    elif from_format == "hex":
        try:
            raw_bytes = binascii.unhexlify(data)
        except Exception as e:
            typer.echo(f"Error decoding hex: {e}", err=True)
            raise typer.Exit(code=1) from e
    elif from_format != "raw":
        typer.echo(f"Unknown source format: {from_format}", err=True)
        raise typer.Exit(code=1)

    if to_format == "raw":
        typer.echo(f"Raw bytes: {raw_bytes!r}")
        typer.echo(f"As string: {raw_bytes.decode(errors='replace')}")
    elif to_format == "base64":
        encoded = base64.b64encode(raw_bytes).decode()
        typer.echo(f"Base64 encoded: {encoded}")
    elif to_format == "hex":
        encoded = binascii.hexlify(raw_bytes).decode()
        typer.echo(f"Hex encoded: {encoded}")
    else:
        typer.echo(f"Unknown target format: {to_format}", err=True)
        raise typer.Exit(code=1)


@app.command()
def option_ascii_replace(
    payload: bytes = typer.Option(
        ...,
        "--payload",
        help="Bytes option encoded with ascii and errors=replace",
        encoding="ascii",
        errors="replace",
    ),
):
    """Demonstrate bytes option with ascii encoding and errors=replace."""
    typer.echo(f"Option bytes: {payload!r}")


if __name__ == "__main__":
    app()
