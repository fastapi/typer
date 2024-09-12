from enum import Enum
from typing import Tuple

import typer
from typing_extensions import Annotated


class SuperHero(str, Enum):
    hero1 = "Superman"
    hero2 = "Spiderman"
    hero3 = "Wonder woman"


def main(
    names: Annotated[
        Tuple[str, str, str, SuperHero],
        typer.Argument(
            enum_by_name=True,
            help="Select 4 characters to play with",
            case_sensitive=False,
        ),
    ] = ("Harry", "Hermione", "Ron", "hero3"),
):
    for name in names:
        if isinstance(name, Enum):
            print(f"Hello {name.value}")
        else:
            print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
