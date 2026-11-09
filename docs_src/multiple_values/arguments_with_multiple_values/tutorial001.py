from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def main(files: list[Path], celebration: str):
    for path in files:
        if path.is_file():
            print(f"This file exists: {path.name}")
            print(celebration)


if __name__ == "__main__":
    app()
