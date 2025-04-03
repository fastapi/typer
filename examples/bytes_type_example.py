import typer
import base64

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


if __name__ == "__main__":
    app()
