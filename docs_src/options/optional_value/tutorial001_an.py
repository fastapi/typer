import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(
    name: str, lastname: str, greeting: Annotated[bool | str, typer.Option()] = "formal"
):
    if not greeting:
        return

    if greeting == "formal":
        print(f"Hello {name} {lastname}")

    elif greeting == "casual":
        print(f"Hi {name} !")

    else:
        raise ValueError(f"Invalid greeting '{greeting}'")


if __name__ == "__main__":
    app()
