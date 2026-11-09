import typer

app = typer.Typer()


@app.command()
def main(
    ID: int = typer.Argument(..., min=0, max=1000),
    age: int = typer.Option(20, min=18),
    score: float = typer.Option(0, max=100),
):
    print(f"ID is {ID}")
    print(f"--age is {age}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
