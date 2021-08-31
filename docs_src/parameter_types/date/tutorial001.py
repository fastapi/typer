from calendar import day_name
from datetime import date

import typer


def main(birth: date):
    typer.echo(f"Interesting day to be born: {birth}")
    typer.echo(f"Birth day name: {day_name[birth.weekday()]}")


if __name__ == "__main__":
    typer.run(main)
