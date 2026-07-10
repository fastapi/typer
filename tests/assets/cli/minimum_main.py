import typer

app = typer.Typer()


@app.callback()
def main(name: str) -> None:
    pass  # pragma: no cover
