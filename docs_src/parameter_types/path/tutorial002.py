from pathlib import Path

import typer


def main(
    config: Path = typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    text = config.read_text()
    typer.echo(f"Config file contents: {text}")


if __name__ == "__main__":
    typer.run(main)
