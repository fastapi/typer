import typer

app = typer.Typer()


@app.command()
def main(config: typer.FileText = typer.Option(..., mode="a")):
    config.write("This is a single line\n")
    print("Config line written")


if __name__ == "__main__":
    app()
