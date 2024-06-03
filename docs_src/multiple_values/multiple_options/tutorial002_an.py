from typing import List

import typer
from typing_extensions import Annotated


def main(number: Annotated[List[float], typer.Option()] = []):
    print(f"The sum is {sum(number)}")


if __name__ == "__main__":
    typer.run(main)
