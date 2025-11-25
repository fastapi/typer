import typer

app = typer.Typer()


@app.command()
def main(
    id: int = typer.Argument(..., min=0, max=1000),
    rank: int = typer.Option(0, max=10, clamp=True),
    score: float = typer.Option(0, min=0, max=100, clamp=True),
):
    print(f"ID is {id}")
    print(f"--rank is {rank}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
