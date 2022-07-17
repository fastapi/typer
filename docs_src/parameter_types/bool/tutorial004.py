import typer


def main(in_prod: bool = typer.Option(True, " /--demo", " /-d")):
    if in_prod:
        print("Running in production")
    else:
        print("Running demo")


if __name__ == "__main__":
    typer.run(main)
