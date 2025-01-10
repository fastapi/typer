import typer
from typing_extensions import Annotated


def main(user_info: Annotated[dict, typer.Option()]):
    print(f"Name: {user_info.get('name', 'Unknown')}")
    print(f"User attributes: {sorted(user_info.keys())}")


if __name__ == "__main__":
    typer.run(main)
