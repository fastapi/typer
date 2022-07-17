import typer


def main(name: str):
    typer.secho(f"Welcome here {name}", fg=typer.colors.MAGENTA)


if __name__ == "__main__":
    typer.run(main)
