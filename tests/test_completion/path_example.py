from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def f(p: Path):
    print(p)


if __name__ == "__main__":
    app()
