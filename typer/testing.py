from collections.abc import Mapping, Sequence
from typing import IO, Any

from click.testing import CliRunner as ClickCliRunner  # noqa
from click.testing import Result
from typer.main import Typer
from typer.main import get_command as _get_command


class CliRunner(ClickCliRunner):
    """A testing helper that invokes Typer CLI applications in isolation.

    This is a thin wrapper around Click's
    [`CliRunner`](https://click.palletsprojects.com/en/stable/api/#click.testing.CliRunner)
    that accepts a `Typer` app instance instead of a raw Click `Command`.

    **Example**

    ```python
    from typer.testing import CliRunner
    import typer

    app = typer.Typer()

    @app.command()
    def hello(name: str):
        print(f"Hello {name}")

    runner = CliRunner()
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
        """Invoke a Typer app in an isolated environment for testing.

        The app is converted to a Click `Command` and then forwarded to
        Click's `CliRunner.invoke`.  This returns a
        [`Result`](https://click.palletsprojects.com/en/stable/api/#click.testing.Result)
        object that gives access to the captured output and exit code.

        Args:
            app: The `Typer` application instance to invoke.
            args: The command-line arguments to pass, as a string or list
                of strings.
            input: Simulated standard-input data (bytes, str, or a
                file-like object).
            env: A mapping of environment variable overrides.
            catch_exceptions: If `True` (the default), exceptions other
                than `SystemExit` are caught and stored on the result
                instead of propagating.
            color: If `True`, output is not stripped of ANSI color codes.
            **extra: Additional keyword arguments forwarded to the
                underlying Click `Command.main`.

        Returns:
            A Click `Result` with the captured output and exit code.
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
