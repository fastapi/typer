import typer
from typing_extensions import Annotated


def main(user_name: Annotated[str, typer.Option("--name", "-n")]):
    print(f"Hello {user_name}")


if __name__ == "__main__":
    typer.run(main)
