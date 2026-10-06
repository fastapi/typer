import pytest
import typer
from typer.exceptions import TyperException
from typer.main import get_command
from typer.testing import CliRunner

runner = CliRunner()


def test_no_prefixed_bool_uses_stripped_negative_flag() -> None:
    app = typer.Typer(add_completion=False)

    @app.command()
    def main(no_force: bool = False) -> None:
        typer.echo(f"{no_force=}")

    command = get_command(app)
    option = next(p for p in command.params if p.name == "no_force")
    assert option.opts == ["--no-force"]
    assert option.secondary_opts == ["--force"]

    assert runner.invoke(app, ["--no-force"]).output.strip() == "no_force=True"
    assert runner.invoke(app, ["--force"]).output.strip() == "no_force=False"
    assert "--no-no-force" not in runner.invoke(app, ["--help"]).output


def test_force_bool_unchanged() -> None:
    app = typer.Typer(add_completion=False)

    @app.command()
    def main(force: bool = False) -> None:
        typer.echo(f"{force=}")

    command = get_command(app)
    option = next(p for p in command.params if p.name == "force")
    assert option.opts == ["--force"]
    assert option.secondary_opts == ["--no-force"]


def test_force_and_no_force_collide_loudly() -> None:
    app = typer.Typer(add_completion=False)

    @app.command()
    def main(force: bool = True, no_force: bool = False) -> None:
        typer.echo(f"{force=} {no_force=}")

    with pytest.raises(TyperException, match="Duplicate CLI option '--no-force'"):
        get_command(app)
