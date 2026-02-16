from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    id: Annotated[int, typer.Argument(min=0, max=1000)],
    rank: Annotated[int, typer.Option(max=10, clamp=True)] = 0,
    score: Annotated[float, typer.Option(min=0, max=100, clamp=True)] = 0,
):
    print(f"ID is {id}")
    print(f"--rank is {rank}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
