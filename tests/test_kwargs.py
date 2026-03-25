import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_kwargs_only() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(**kwargs: str) -> None:
        typer.echo(f"kwargs={kwargs!r}")

    result = runner.invoke(app, ["--flag", "val", "--verbose"])
    assert result.exit_code == 0
    assert "flag" in result.output
    assert "val" in result.output
    assert "verbose" in result.output


def test_kwargs_bool_flag() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(**kwargs: str) -> None:
        import json

        typer.echo(json.dumps(kwargs))

    result = runner.invoke(app, ["--bool-flag"])
    assert result.exit_code == 0
    assert '"bool_flag": true' in result.output


def test_args_only() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: str) -> None:
        typer.echo(f"args={args!r}")

    result = runner.invoke(app, ["--", "opt1", "opt2"])
    assert result.exit_code == 0
    assert "opt1" in result.output
    assert "opt2" in result.output


def test_args_and_kwargs_together() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: str, **kwargs: str) -> None:
        typer.echo(f"args={args!r} kwargs={kwargs!r}")

    result = runner.invoke(app, ["--flag", "val", "--", "opt1", "opt2"])
    assert result.exit_code == 0
    assert "opt1" in result.output
    assert "opt2" in result.output
    assert "flag" in result.output
    assert "val" in result.output


def test_kwargs_before_mandatory_positional() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(name: str, **kwargs: str) -> None:
        typer.echo(f"name={name!r} kwargs={kwargs!r}")

    result = runner.invoke(app, ["--flag", "val", "Bob"])
    assert result.exit_code == 0
    assert "name='Bob'" in result.output
    assert "flag" in result.output
    assert "val" in result.output


def test_double_dash_no_args() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: str, **kwargs: str) -> None:
        typer.echo(f"args={args!r}")

    result = runner.invoke(app, ["--"])
    assert result.exit_code == 0
    assert "args=()" in result.output


def test_no_extra_args() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(*args: str, **kwargs: str) -> None:
        typer.echo(f"args={args!r} kwargs={kwargs!r}")

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "args=()" in result.output
    assert "kwargs={}" in result.output


def test_known_options_still_work() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(name: str, count: int = 1, **kwargs: str) -> None:
        typer.echo(f"name={name!r} count={count!r} kwargs={kwargs!r}")

    result = runner.invoke(app, ["--count", "3", "--extra", "foo", "Alice"])
    assert result.exit_code == 0
    assert "name='Alice'" in result.output
    assert "count=3" in result.output
    assert "extra" in result.output
    assert "foo" in result.output


def test_regression_no_variadics() -> None:
    """Functions without *args/**kwargs should be unaffected."""
    app = typer.Typer()

    @app.command()
    def cmd(name: str, count: int = 1) -> None:
        typer.echo(f"name={name!r} count={count!r}")

    result = runner.invoke(app, ["--count", "5", "Bob"])
    assert result.exit_code == 0
    assert "name='Bob'" in result.output
    assert "count=5" in result.output


def test_all_together() -> None:
    app = typer.Typer()

    @app.command()
    def cmd(mandatory: str, *args: str, **kwargs: str) -> None:
        typer.echo(f"mandatory={mandatory!r} args={args!r} kwargs={kwargs!r}")

    result = runner.invoke(
        app, ["--flag1", "val", "--bool-flag", "mandatory-arg", "--", "opt1", "opt2"]
    )
    assert result.exit_code == 0
    assert "mandatory='mandatory-arg'" in result.output
    assert "opt1" in result.output
    assert "opt2" in result.output
    assert "flag1" in result.output
    assert "val" in result.output
    assert "bool_flag" in result.output
