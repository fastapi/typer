import typer


def main(project_name: str = typer.Option(..., prompt=True, confirmation_prompt=True)):
    typer.echo(f"Deleting project {project_name}")


if __name__ == "__main__":
    typer.run(main)
