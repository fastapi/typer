from enum import Enum

import typer


class Interval(Enum):
    ONE_MINUTE = "1m"
    ONE_MONTH = "1M"
    OTHER = "o"


def main(
    interval: Interval = typer.Option(Interval.OTHER, case_sensitive=True)
):
    print(f"Found interval: {interval.value}")


if __name__ == "__main__":
    typer.run(main)
