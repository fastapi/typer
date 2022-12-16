import typer


def main(config: typer.FileText = typer.Option(...)):
    for line in config:
        print(f"Config line: {line}")


if __name__ == "__main__":
    typer.run(main)
