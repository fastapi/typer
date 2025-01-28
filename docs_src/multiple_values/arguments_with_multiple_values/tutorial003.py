from enum import Enum
from typing import Tuple

import typer


class SuperHero(str, Enum):
    hero1 = "Superman"
    hero2 = "Spiderman"
    hero3 = "Wonder woman"


def main(
    names: Tuple[str, str, str, SuperHero] = typer.Argument(
        ("Harry", "Hermione", "Ron", "hero3"),
        enum_by_name=True,
        case_sensitive=False,
        help="Select 4 characters to play with",
    ),
):
    for name in names:
        if isinstance(name, Enum):
            print(f"Hello {name.value}")
        else:
            print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
