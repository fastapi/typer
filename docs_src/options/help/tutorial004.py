import typer


def main(
    fullname: str = typer.Option(
        "Wade Wilson", show_default="Deadpoolio the amazing's name"
    ),
):
    print(f"Hello {fullname}")


if __name__ == "__main__":
    typer.run(main)
