import typer

app = typer.Typer()


@app.command()
def main(name: list[str] = typer.Option(["World"], help="The name to say hi to.")):
    for each_name in name:
        print(f"Hello {each_name}")


if __name__ == "__main__":
    app()
