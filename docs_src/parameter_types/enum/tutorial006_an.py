from enum import Enum
from typing import List

import typer
from typing_extensions import Annotated


class Food(str, Enum):
    f1 = "Eggs"
    f2 = "Bacon"
    f3 = "Cheese"


def main(
    groceries: Annotated[List[Food], typer.Option(enum_by_name=True)] = ["f1", "f3"],
):
    print(f"Buying groceries: {', '.join([f.value for f in groceries])}")


if __name__ == "__main__":
    typer.run(main)
