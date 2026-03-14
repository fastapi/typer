import typer

app = typer.Typer()


@app.command()
def main(
    name: str = typer.Option(..., "--name", "-n"),
    formal: bool = typer.Option(False, "--formal", "-f"),
):
    if formal:
        print(f"Good day Ms. {name}.")
    else:
        print(f"Hello {name}")


if __name__ == "__main__":
    app()
