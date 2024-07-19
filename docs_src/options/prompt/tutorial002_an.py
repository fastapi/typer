import typer
from typing_extensions import Annotated


def main(
    name: str,
    lastname: Annotated[str, typer.Option(prompt="Please tell me your last name")],
):
    print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    typer.run(main)
