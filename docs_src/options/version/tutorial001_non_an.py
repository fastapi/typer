import typer

__version__ = "0.1.0"

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    name: str = typer.Option("World"),
    version: bool | None = typer.Option(None, "--version", callback=version_callback),
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
