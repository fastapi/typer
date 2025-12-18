import time

import typer
from rich.progress import track

app = typer.Typer()


@app.command()
def main():
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")


if __name__ == "__main__":
    app()
