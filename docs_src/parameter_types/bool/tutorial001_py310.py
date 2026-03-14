import typer

app = typer.Typer()


@app.command()
def main(force: bool = typer.Option(False, "--force")):
    if force:
        print("Forcing operation")
    else:
        print("Not forcing")


if __name__ == "__main__":
    app()
