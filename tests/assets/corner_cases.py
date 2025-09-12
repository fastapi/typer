import typer

app = typer.Typer()


@app.command(context_settings={"auto_envvar_prefix": "TEST"})
def main(
    name: str = typer.Option("John", hidden=True),
    lastname: str = typer.Option("Doe", "/lastname", show_default="Mr. Doe"),
    age: int = typer.Option(lambda: 42, show_default=True),
):
    """
    Say hello.
    """
    print(f"Hello {name} {lastname}, it seems you have {age}")


if __name__ == "__main__":
    app()
