import typer

image_desc = [
    ("alpine-latest-333", "latest alpine image"),
    ("alpine-hello-666", "fake image: for testing"),
    ("something-else-999", "yet another image"),
]


def _complete(incomplete: str) -> str:
    for image, desc in image_desc:
        if image.startswith(incomplete):
            yield image, desc


app = typer.Typer()


@app.command()
def image(name: str = typer.Option(autocompletion=_complete)):
    typer.echo(name)


if __name__ == "__main__":
    app()
