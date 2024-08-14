from typing import Optional

import typer


def main(name: Optional[str] = typer.Argument(default=None)):
    if name is None:
        print("Hello World!")
    else:
        print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
