from datetime import date

import typer


def main(launch_date: date = typer.Argument(..., formats=["%Y-%m-%d", "%m/%d/%Y"])):
    typer.echo(f"Launch will be at: {launch_date}")


if __name__ == "__main__":
    typer.run(main)
