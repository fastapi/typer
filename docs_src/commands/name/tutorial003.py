import typer

app = typer.Typer()


@app.command("list", "ls", hidden_aliases=["secretlist"])
def list_items():
    print("Listing items")


@app.command("remove")
def remove_items():
    print("Removing items")


if __name__ == "__main__":
    app()
