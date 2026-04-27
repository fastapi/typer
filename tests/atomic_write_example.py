import time

import typer

app = typer.Typer()


@app.command()
def write_atomic(
    config: typer.FileText = typer.Option(..., mode="w", atomic=True),
    pause: float = typer.Option(0.3),
) -> None:
    config.write("atomic-content-1\n")
    config.flush()
    typer.echo("halfway")
    time.sleep(pause)
    config.write("atomic-content-2\n")
    config.flush()
    typer.echo("written atomically")


@app.command()
def write_atomic_binary(
    config: typer.FileBinaryWrite = typer.Option(..., atomic=True, lazy=False),
) -> None:
    config.write(b"\x00\x01binary-atomic\n")
    typer.echo("written binary atomically")


@app.command()
def api_atomic(
    config: typer.FileText = typer.Option(..., mode="w", atomic=True, lazy=False),
) -> None:
    typer.echo(f"name={config.name}")
    typer.echo(f"repr={repr(config)}")
    with config as entered:
        typer.echo(f"entered={entered is config}")
        entered.write("atomic-api-done\n")


@app.command()
def invalid_atomic_append(
    config: typer.FileText = typer.Option(..., mode="a", atomic=True, lazy=False),
) -> None:
    typer.echo(config.name)  # pragma: no cover


@app.command()
def invalid_atomic_exclusive(
    config: typer.FileText = typer.Option(..., mode="x", atomic=True, lazy=False),
) -> None:
    typer.echo(config.name)  # pragma: no cover


@app.command()
def invalid_atomic_read(
    config: typer.FileText = typer.Option(..., mode="r", atomic=True, lazy=False),
) -> None:
    typer.echo(config.name)  # pragma: no cover


if __name__ == "__main__":
    app()
