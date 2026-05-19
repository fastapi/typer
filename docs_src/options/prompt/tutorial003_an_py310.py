from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    project_name: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True)],
):
    print(f"Deleting project {project_name}")


if __name__ == "__main__":
    app()
