import typer
from typing_extensions import Annotated


def main(config: Annotated[typer.FileTextWrite, typer.Option()]):
    config.write("Some config written by the app")
    print("Config written")


if __name__ == "__main__":
    typer.run(main)
