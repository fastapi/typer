import typer

app = typer.Typer()


@app.command()
def main(config: typer.FileText = typer.Option(...)):
    print(config.read())


if __name__ == "__main__":
    app()
