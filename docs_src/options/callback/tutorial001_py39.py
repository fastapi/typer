from typing import Optional

import typer

app = typer.Typer()


def name_callback(value: str):
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


@app.command()
def main(name: Optional[str] = typer.Option(default=None, callback=name_callback)):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
