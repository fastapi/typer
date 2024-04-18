import typer


def main(name: str, lastname: str = typer.Option(default=...)):
    print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    typer.run(main)
