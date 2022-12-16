import typer


def main(name: str = typer.Argument("Wade Wilson")):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
