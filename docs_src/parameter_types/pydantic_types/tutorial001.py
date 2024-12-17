import typer
from pydantic import AnyHttpUrl


def main(url_arg: AnyHttpUrl):
    typer.echo(f"url_arg: {url_arg}")


if __name__ == "__main__":
    typer.run(main)
