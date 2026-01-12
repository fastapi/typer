import typer

app = typer.Typer()


@app.command()
def main(verbose: int = typer.Option(0, "--verbose", "-v", count=True)):
    print(f"Verbose level is {verbose}")


if __name__ == "__main__":
    app()
