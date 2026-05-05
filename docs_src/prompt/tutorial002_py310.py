import typer

app = typer.Typer()


@app.command()
def main():
    delete = typer.confirm("Are you sure you want to delete it?")
    if not delete:
        print("Not deleting")
        raise typer.Abort()
    print("Deleting it!")


if __name__ == "__main__":
    app()
