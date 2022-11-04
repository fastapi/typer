import typer
import typer.main

typer.main.rich = None


def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    typer.run(main)
