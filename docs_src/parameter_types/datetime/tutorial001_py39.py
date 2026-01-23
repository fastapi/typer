from datetime import datetime

import typer

app = typer.Typer()


@app.command()
def main(birth: datetime):
    print(f"Interesting day to be born: {birth}")
    print(f"Birth hour: {birth.hour}")


if __name__ == "__main__":
    app()
