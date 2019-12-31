import typer


def main(
    id: int = typer.Argument(..., min=0, max=1000),
    age: int = typer.Option(20, min=18),
    score: float = typer.Option(0, max=100),
):
    typer.echo(f"ID is {id}")
    typer.echo(f"--age is {age}")
    typer.echo(f"--score is {score}")


if __name__ == "__main__":
    typer.run(main)
