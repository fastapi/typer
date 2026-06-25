import base64

import typer

app = typer.Typer()


@app.command()
def encode(text: bytes):
    """Encode text to base64."""
    encoded = base64.b64encode(text)
    typer.echo(f"Original: {text!r}")
    typer.echo(f"Encoded: {encoded.decode()}")


@app.command()
def decode(encoded: str):
    """Decode base64 to bytes."""
    decoded = base64.b64decode(encoded)
    typer.echo(f"Encoded: {encoded}")
    typer.echo(f"Decoded: {decoded!r}")


@app.command()
def echo_default(
    name: bytes = typer.Argument(..., help="Name as bytes (default UTF-8)"),
):
    """Echo bytes with default UTF-8 encoding."""
    typer.echo(f"Default UTF-8 bytes: {name!r}")


@app.command()
def echo_latin1(
    name: bytes = typer.Argument(
        ..., encoding="latin-1", help="Name as bytes (latin-1)"
    ),
):
    """Echo bytes with latin-1 encoding for the argument."""
    typer.echo(f"Latin-1 bytes: {name!r}")


@app.command()
def option_ascii_replace(
    token: bytes = typer.Option(
        ...,
        "--token",
        encoding="ascii",
        errors="replace",
        help="Token as bytes (ascii, errors=replace)",
    ),
):
    """Option demonstrating ascii encoding with errors=replace."""
    typer.echo(f"Option bytes: {token!r}")


if __name__ == "__main__":
    app()
