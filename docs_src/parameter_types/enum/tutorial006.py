from enum import Enum
from typing import List

import typer


class Food(str, Enum):
    f1 = "Eggs"
    f2 = "Bacon"
    f3 = "Cheese"


def main(groceries: List[Food] = typer.Option(["f1", "f3"], enum_by_name=True)):
    print(f"Buying groceries: {', '.join([f.value for f in groceries])}")


if __name__ == "__main__":
    typer.run(main)
