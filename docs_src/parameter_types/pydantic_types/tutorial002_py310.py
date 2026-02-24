import typer
from pydantic import AnyHttpUrl

app = typer.Typer()


@app.command()
def main(url_opt: AnyHttpUrl = typer.Option("https://typer.tiangolo.com")):
    typer.echo(f"url_opt: {url_opt}")


if __name__ == "__main__":
    app()
