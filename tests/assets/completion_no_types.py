import typer

app = typer.Typer()


def complete(ctx, args, incomplete):
    typer.echo(f"info name is: {ctx.info_name}", err=True)
    typer.echo(f"args is: {args}", err=True)
    typer.echo(f"incomplete is: {incomplete}", err=True)
    return [
        ("Camila", "The reader of books."),
        ("Carlos", "The writer of scripts."),
        ("Sebastian", "The type hints guy."),
    ]


@app.command()
def main(name: str = typer.Option("World", autocompletion=complete)):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
