import typer


def main(name: str = typer.Argument(default=...)):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
