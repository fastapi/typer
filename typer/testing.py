"""Testing utilities for Typer applications.

Provides a `CliRunner` that wraps Click's test runner with Typer-aware
`invoke`, so you can test `Typer` apps directly without converting them
to Click commands by hand.

Read more in the
[Typer docs for Testing](https://typer.tiangolo.com/tutorial/testing/).
"""

from collections.abc import Mapping, Sequence
from typing import IO, Any

from click.testing import CliRunner as ClickCliRunner  # noqa
from click.testing import Result
from typer.main import Typer
from typer.main import get_command as _get_command


class CliRunner(ClickCliRunner):
    """A test runner for `Typer` applications.

    Extends Click's `CliRunner` with a Typer-aware `invoke` method that
    accepts a `Typer` instance directly, removing the need to call
    `typer.main.get_command` in every test.

    Read more in the
    [Typer docs for Testing](https://typer.tiangolo.com/tutorial/testing/).

    ## Example

    ```python
    from typer.testing import CliRunner
    import typer

    app = typer.Typer()

    @app.command()
    def hello(name: str) -> None:
        typer.echo(f"Hello {name}")

    runner = CliRunner()

    def test_hello() -> None:
        result = runner.invoke(app, ["World"])
        assert result.exit_code == 0
        assert "Hello World" in result.output
    ```
    """

    def invoke(  # type: ignore
        self,
        app: Typer,
        args: str | Sequence[str] | None = None,
        input: bytes | str | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        catch_exceptions: bool = True,
        color: bool = False,
        **extra: Any,
    ) -> Result:
        """Invoke a `Typer` app in an isolated environment for testing.

        Converts the `Typer` instance to a Click command and delegates to
        Click's `CliRunner.invoke`.

        Read more in the
        [Typer docs for Testing](https://typer.tiangolo.com/tutorial/testing/).
        """
        use_cli = _get_command(app)
        return super().invoke(
            use_cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            color=color,
            **extra,
        )
