import time

import typer

app = typer.Typer()


@app.command()
def main():
    total = 0
    with typer.progressbar(range(100), label="Processing") as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.01)
            total += 1
    print(f"Processed {total} things.")


if __name__ == "__main__":
    app()
