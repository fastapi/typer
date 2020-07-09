import typer


def main(
    id: int = typer.Argument(..., min=0, max=1000),
    rank: int = typer.Option(0, max=10, clamp=True),
    score: float = typer.Option(0, min=0, max=100, clamp=True),
):
    typer.echo(f"ID is {id}")
    typer.echo(f"--rank is {rank}")
    typer.echo(f"--score is {score}")


if __name__ == "__main__":
    typer.run(main)
