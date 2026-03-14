from enum import Enum
from typing import Annotated

import typer


class Food(str, Enum):
    food_1 = "Eggs"
    food_2 = "Bacon"
    food_3 = "Cheese"


app = typer.Typer()


@app.command()
def main(groceries: Annotated[list[Food], typer.Option()] = [Food.food_1, Food.food_3]):
    print(f"Buying groceries: {', '.join([f.value for f in groceries])}")


if __name__ == "__main__":
    app()
