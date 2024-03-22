from typing import List, Optional

import typer
from typing_extensions import Annotated


def main(user: Annotated[Optional[List[str]], typer.Option()] = None):
    if not user:
        print("No provided users")
        raise typer.Abort()
    for u in user:
        print(f"Processing user: {u}")


if __name__ == "__main__":
    typer.run(main)
