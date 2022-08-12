import typer


def main(fullname: str = typer.Option("Wade Wilson", show_default=False)):
    print(f"Hello {fullname}")


if __name__ == "__main__":
    typer.run(main)
