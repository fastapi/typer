from typing import Optional

import typer


def name_callback(value: str):
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


def main(name: Optional[str] = typer.Option(default=None, callback=name_callback)):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
