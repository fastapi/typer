from typing import Optional

import typer
from typing_extensions import Annotated


def name_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    print("Validating name")
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


def main(name: Annotated[Optional[str], typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
