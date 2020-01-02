import typer


def main():
    person_name = typer.prompt("What's your name?")
    typer.echo(f"Hello {person_name}")


if __name__ == "__main__":
    typer.run(main)
