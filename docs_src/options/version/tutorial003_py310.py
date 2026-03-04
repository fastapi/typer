import typer

__version__ = "0.1.0"

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def name_callback(name: str):
    if name != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return name


@app.command()
def main(
    name: str = typer.Option(..., callback=name_callback),
    version: bool | None = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
