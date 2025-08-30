import sys

import typer

app = typer.Typer()


@app.command()
def main():
    for m in sys.modules:
        print(m)


if __name__ == "__main__":
    app()
