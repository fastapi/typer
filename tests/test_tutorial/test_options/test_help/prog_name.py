import typer

app = typer.Typer()


@app.command()
def main(i: int):
    pass


if __name__ == "__main__":
    app(prog_name="custom-name")
