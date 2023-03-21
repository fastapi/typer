from enum import Enum

import typer
from typer.testing import CliRunner

runner = CliRunner()
app = typer.Typer()


class Case(str, Enum):
    UPPER = "CASE"
    TITLE = "Case"
    LOWER = "case"

    def __str__(self) -> str:
        return self.value


@app.command()
def enum_case(case: Case):
    print(case)


if __name__ == "__main__":
    app()
