from typing import Annotated

import typer

app = typer.Typer()


def name_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    print("Validating name")
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


@app.command()
def main(name: Annotated[str | None, typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
