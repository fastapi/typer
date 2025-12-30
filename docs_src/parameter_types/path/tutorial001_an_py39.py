from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer()


@app.command()
def main(config: Annotated[Optional[Path], typer.Option()] = None):
    if config is None:
        print("No config file")
        raise typer.Abort()
    if config.is_file():
        text = config.read_text()
        print(f"Config file contents: {text}")
    elif config.is_dir():
        print("Config is a directory, will use all its config files")
    elif not config.exists():
        print("The config doesn't exist")


if __name__ == "__main__":
    app()
