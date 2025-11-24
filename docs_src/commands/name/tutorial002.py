import typer

app = typer.Typer()


@app.command("list", "ls")
def list_items():
    print("Listing items")


@app.command("remove", aliases=["rm", "delete"])
def remove_items():
    print("Removing items")


if __name__ == "__main__":
    app()
