from enum import StrEnum
from typing import Annotated

import typer


class Food(StrEnum):
    food_1 = "Eggs"
    food_2 = "Bacon"
    food_3 = "Cheese"


app = typer.Typer()


@app.command()
def main(groceries: Annotated[list[Food], typer.Option()] = [Food.food_1, Food.food_3]):
    print(f"Buying groceries: {', '.join(groceries)}")


if __name__ == "__main__":
    app()
