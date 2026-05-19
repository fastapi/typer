from enum import Enum
from typing import Annotated

import typer


class Food(str, Enum):
    f1 = "Eggs"
    f2 = "Bacon"
    f3 = "Cheese"


app = typer.Typer()


@app.command()
def main(
    groceries: Annotated[list[Food], typer.Option(enum_by_name=True)] = ["f1", "f3"],
):
    print(f"Buying groceries: {', '.join([f.value for f in groceries])}")


if __name__ == "__main__":
    app()
