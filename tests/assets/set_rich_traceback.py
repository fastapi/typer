import typer

typer.set_rich_traceback(False)

app = typer.Typer()


@app.command()
def raise_():
    raise ValueError  # raise some error to test traceback output


if __name__ == "__main__":
    app()
