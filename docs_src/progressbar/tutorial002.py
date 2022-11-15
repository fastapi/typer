import time

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn


def main():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        progress.add_task(description="Preparing...", total=None)
        time.sleep(5)
    print("Done!")


if __name__ == "__main__":
    typer.run(main)
