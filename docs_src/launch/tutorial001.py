import typer


def main():
    typer.echo("Opening Typer's docs")
    typer.launch("https://typer.tiangolo.com")


if __name__ == "__main__":
    typer.run(main)
