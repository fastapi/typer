from enum import StrEnum

import typer


class Food(StrEnum):
    food_1 = "Eggs"
    food_2 = "Bacon"
    food_3 = "Cheese"


app = typer.Typer()


@app.command()
def main(groceries: list[Food] = typer.Option([Food.food_1, Food.food_3])):
    print(f"Buying groceries: {', '.join(groceries)}")


if __name__ == "__main__":
    app()
