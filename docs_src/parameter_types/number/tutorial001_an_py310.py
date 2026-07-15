from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    ID: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"ID is {ID}")
    print(f"--age is {age}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
