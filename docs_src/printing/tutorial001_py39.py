import typer
from rich import print

data = {
    "name": "Rick",
    "age": 42,
    "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
    "active": True,
    "affiliation": None,
}

app = typer.Typer()


@app.command()
def main():
    print("Here's the data")
    print(data)


if __name__ == "__main__":
    app()
