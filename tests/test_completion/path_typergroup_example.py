import click
import typer
import typer.core


class DynamicGroup(typer.core.TyperGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_command(process_cmd, "process")


process_cmd = click.Command(
    name="process",
    callback=lambda **kw: print(kw),
    params=[
        click.Option(
            ["--input", "-i"],
            type=click.Path(exists=False),
            required=True,
            help="Input file",
        ),
        click.Option(
            ["--output-dir", "-o"],
            type=click.Path(file_okay=False, dir_okay=True),
            help="Output directory",
        ),
        click.Option(
            ["--count", "-n"],
            type=int,
            default=1,
            help="Number of items",
        ),
    ],
)

app = typer.Typer()
sub_app = typer.Typer(cls=DynamicGroup)
app.add_typer(sub_app, name="sub")

if __name__ == "__main__":
    app()
