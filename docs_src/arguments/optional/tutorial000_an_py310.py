from typing import Annotated

import typer


def main(name: Annotated[str, typer.Argument()]):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
