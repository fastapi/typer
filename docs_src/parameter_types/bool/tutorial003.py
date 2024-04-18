import typer


def main(force: bool = typer.Option(False, "--force/--no-force", "-f/-F")):
    if force:
        print("Forcing operation")
    else:
        print("Not forcing")


if __name__ == "__main__":
    typer.run(main)
