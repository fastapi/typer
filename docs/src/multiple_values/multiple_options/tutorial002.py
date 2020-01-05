from typing import List

import typer


def main(number: List[float] = typer.Option([])):
    typer.echo(f"The sum is {sum(number)}")


if __name__ == "__main__":
    typer.run(main)
