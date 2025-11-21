from typing import Optional

import typer
from typing_extensions import Annotated

app = typer.Typer()


def name_callback(value: str):
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


@app.command()
def main(name: Annotated[Optional[str], typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
