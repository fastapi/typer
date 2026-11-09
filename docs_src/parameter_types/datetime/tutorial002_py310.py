from datetime import datetime

import typer

app = typer.Typer()


@app.command()
def main(
    launch_date: datetime = typer.Argument(..., formats=["%Y-%m-%d", "%m/%d/%Y"]),
):
    print(f"Launch will be at: {launch_date}")


if __name__ == "__main__":
    app()
