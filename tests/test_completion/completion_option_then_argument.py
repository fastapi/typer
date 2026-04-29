import typer

app = typer.Typer()


def complete_name(ctx, args, incomplete):
    return ["opt-choice"]  # pragma: no cover


def complete_target(ctx, args, incomplete):
    return ["arg-choice"]


@app.command()
def main(
    name: str = typer.Option(..., "--name", autocompletion=complete_name),
    target: str = typer.Argument(..., autocompletion=complete_target),
):
    print(name, target)  # pragma: no cover


if __name__ == "__main__":
    app()
