import typer

app = typer.Typer()


@app.command()
def main(number: list[float] = typer.Option([])):
    print(f"The sum is {sum(number)}")


if __name__ == "__main__":
    app()
