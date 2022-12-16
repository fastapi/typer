import typer


def main(name: str = typer.Argument(..., help="The name of the user to greet")):
    """
    Say hi to NAME very gently, like Dirk.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
