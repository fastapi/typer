from typing import Annotated

import typer

app = typer.Typer(align_panel_columns=True, add_completion=False)


@app.command()
def main(
    source: Annotated[str, typer.Argument(help="Source path.")],
    dest: Annotated[str, typer.Argument(help="Destination path.")] = "",
    short_flag: Annotated[
        bool, typer.Option("-a", help="Short flag.", rich_help_panel="Short")
    ] = False,
    short_value: Annotated[
        str, typer.Option("-b", help="Short value.", rich_help_panel="Short")
    ] = "",
    mixed_value: Annotated[
        str,
        typer.Option(
            "--mixed-long", "-m", help="Mixed value.", rich_help_panel="Mixed"
        ),
    ] = "",
    mixed_flag: Annotated[
        bool,
        typer.Option("--mixed-flag", "-f", help="Mixed flag.", rich_help_panel="Mixed"),
    ] = False,
    long_value: Annotated[
        str, typer.Option("--alpha", help="Long value.", rich_help_panel="Long")
    ] = "",
    long_flag: Annotated[
        bool, typer.Option("--beta", help="Long flag.", rich_help_panel="Long")
    ] = False,
) -> None:
    pass


if __name__ == "__main__":
    app()
