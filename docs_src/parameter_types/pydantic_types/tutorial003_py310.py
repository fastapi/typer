import typer
from pydantic import AnyHttpUrl

app = typer.Typer()


@app.command()
def main(urls: list[AnyHttpUrl] = typer.Option([], "--url")):
    typer.echo(f"urls: {urls}")


if __name__ == "__main__":
    app()
