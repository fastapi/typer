import typer


def main():
    typer.echo(f"Here is something written to standard error", err=True)


if __name__ == "__main__":
    typer.run(main)
