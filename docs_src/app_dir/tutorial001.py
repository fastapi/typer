from pathlib import Path

import typer

APP_NAME = "my-super-cli-app"


def main():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        typer.echo("Config file doesn't exist yet")


if __name__ == "__main__":
    typer.run(main)
