import typer

typer.enable_rich_help(False)

app = typer.Typer()


@app.command()
def main(arg: str):  # pragma: no cover
    pass


if __name__ == "__main__":
    app()
