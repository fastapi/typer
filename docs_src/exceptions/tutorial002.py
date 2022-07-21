import typer

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(password: str):
    print(password + 3)


if __name__ == "__main__":
    app()
