from datetime import datetime

import typer


def main(
    launch_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
    )
):
    typer.echo(f"Launch will be at: {launch_date}")


if __name__ == "__main__":
    typer.run(main)
