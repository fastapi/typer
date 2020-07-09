from datetime import datetime

import typer


def main(birth: datetime):
    typer.echo(f"Interesting day to be born: {birth}")
    typer.echo(f"Birth hour: {birth.hour}")


if __name__ == "__main__":
    typer.run(main)
