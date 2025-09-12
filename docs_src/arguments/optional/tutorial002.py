import typer


def main(name: str = typer.Argument(default="World")):
    print(f"Hello {name}!")


if __name__ == "__main__":
    typer.run(main)
