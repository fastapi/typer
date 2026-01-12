import typer

app = typer.Typer()


@app.command()
def main(in_prod: bool = typer.Option(True, " /--demo", " /-d")):
    if in_prod:
        print("Running in production")
    else:
        print("Running demo")


if __name__ == "__main__":
    app()
