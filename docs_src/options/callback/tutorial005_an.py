from typing import List, Optional

import typer
from typing_extensions import Annotated


def names_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if ctx.resilient_parsing:
        return
    print(f"Validating param: {param.name}")
    if value is None:
        return value
    if "Camila" not in value:
        raise typer.BadParameter("Camila must be in the list")
    return value


def main(
    names: Annotated[
        Optional[List[str]], typer.Option("--name", callback=names_callback)
    ] = None,
):
    if names is None:
        print("No names provided")
    else:
        print("Hello {}".format(", ".join(names)))


if __name__ == "__main__":
    typer.run(main)
