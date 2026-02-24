from pathlib import Path

import typer

APP_NAME = "my-super-cli-app"

app = typer.Typer()


@app.command()
def main():
    app_dir = typer.get_app_dir(APP_NAME)
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        config_path.write_text('{"version": "1.0.0"}')
    config_file_str = str(config_path)
    print("Opening config directory")
    typer.launch(config_file_str, locate=True)


if __name__ == "__main__":
    app()
