import time

import typer


def main():
    total = 1000
    with typer.progressbar(length=total) as progress:
        for batch in range(4):
            # Fake processing time
            time.sleep(1)
            progress.update(250)
    print(f"Processed {total} things in batches.")


if __name__ == "__main__":
    typer.run(main)
