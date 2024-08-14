import typer


def main(name: str = typer.Argument("World", envvar="AWESOME_NAME")):
    print(f"Hello Mr. {name}")


if __name__ == "__main__":
    typer.run(main)
