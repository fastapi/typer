import typer

app = typer.Typer()


@app.command()
def main(
    id: int = typer.Argument(..., min=0, max=1000),
    age: int = typer.Option(20, min=18),
    score: float = typer.Option(0, max=100),
):
    print(f"ID is {id}")
    print(f"--age is {age}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
