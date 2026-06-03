import typer

from typer.core import TyperCommand, TyperOption, TyperGroup
from typer.models import TyperPath


class DynamicGroup(TyperGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_command(process_cmd, "process")


process_cmd = TyperCommand(
    name="process",
    callback=lambda **kw: print(kw),
    params=[
        TyperOption(
            param_decls=["--input", "-i"],
            type=TyperPath(exists=False),
            required=True,
            help="Input file",
        ),
        TyperOption(
            param_decls=["--output-dir", "-o"],
            type=TyperPath(file_okay=False, dir_okay=True),
            help="Output directory",
        ),
        TyperOption(
            param_decls=["--count", "-n"],
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
