from enum import Enum
from typing import Tuple

import typer


class Food(str, Enum):
    f1 = "Eggs"
    f2 = "Bacon"
    f3 = "Cheese"


def main(user: Tuple[str, int, bool, Food] = typer.Option((None, None, None, Food.f1))):
    username, coins, is_wizard, food = user
    if not username:
        print("No user provided")
        raise typer.Abort()
    print(f"The username {username} has {coins} coins")
    if is_wizard:
        print("And this user is a wizard!")
    print(f"And they love eating {food.value}")


if __name__ == "__main__":
    typer.run(main)
