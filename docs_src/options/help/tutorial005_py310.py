import typer

app = typer.Typer(align_panel_columns=True, add_completion=False)


@app.command()
def main(
    source: str = typer.Argument(help="Source path."),
    dest: str = typer.Argument("", help="Destination path."),
    short_flag: bool = typer.Option(
        False, "-a", help="Short flag.", rich_help_panel="Short"
    ),
    short_value: str = typer.Option(
        "", "-b", help="Short value.", rich_help_panel="Short"
    ),
    mixed_value: str = typer.Option(
        "", "--mixed-long", "-m", help="Mixed value.", rich_help_panel="Mixed"
    ),
    mixed_flag: bool = typer.Option(
        False, "--mixed-flag", "-f", help="Mixed flag.", rich_help_panel="Mixed"
    ),
    long_value: str = typer.Option(
        "", "--alpha", help="Long value.", rich_help_panel="Long"
    ),
    long_flag: bool = typer.Option(
        False, "--beta", help="Long flag.", rich_help_panel="Long"
    ),
) -> None:
    pass


if __name__ == "__main__":
    app()
