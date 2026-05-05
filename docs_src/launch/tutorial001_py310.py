import typer

app = typer.Typer()


@app.command()
def main():
    print("Opening Typer's docs")
    typer.launch("https://typer.tiangolo.com")


if __name__ == "__main__":
    app()
