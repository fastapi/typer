import typer


def main(
    name: str = typer.Argument(
        "Wade Wilson", help="Who to greet", show_default="Deadpoolio the amazing's name"
    )
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
