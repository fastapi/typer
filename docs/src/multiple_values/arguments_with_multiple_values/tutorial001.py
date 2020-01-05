from pathlib import Path
from typing import List

import typer


def main(files: List[Path], celebration: str):
    for path in files:
        if path.is_file():
            typer.echo(f"This file exists: {path.name}")
            typer.echo(celebration)


if __name__ == "__main__":
    typer.run(main)
