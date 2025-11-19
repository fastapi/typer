import typer
import typer.main

typer.main.HAS_RICH = False


def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    typer.run(main)
