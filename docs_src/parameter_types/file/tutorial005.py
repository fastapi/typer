import typer


def main(config: typer.FileText = typer.Option(..., mode="a")):
    config.write("This is a single line\n")
    typer.echo("Config line written")


if __name__ == "__main__":
    typer.run(main)
