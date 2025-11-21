import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(
    id: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"ID is {id}")
    print(f"--age is {age}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
