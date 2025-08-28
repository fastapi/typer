import typer

image_desc = [
    ("alpine:latest", "latest alpine image"),
    ("alpine:hello", "fake image: for testing"),
    ("nvidia/cuda:10.0-devel-ubuntu18.04", ""),
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
