import time

import typer

app = typer.Typer()


@app.command()
def main():
    total = 1000
    with typer.progressbar(length=total) as progress:
        for batch in range(4):
            # Fake processing time
            time.sleep(1)
            # Increment by 250 on each loop iteration
            # (it will take 4 seconds to reach 1000)
            progress.update(250)
    print(f"Processed {total} things in batches.")


if __name__ == "__main__":
    app()
