import typer
from typing_extensions import Annotated


def main(
    name: Annotated[str, typer.Option("--name", "-n")],
    formal: Annotated[bool, typer.Option("--formal", "-f")] = False,
):
    if formal:
        print(f"Good day Ms. {name}.")
    else:
        print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
