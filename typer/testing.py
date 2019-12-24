from typing import IO, Any, Iterable, Mapping, Optional, Text, Union

from click.testing import CliRunner as ClickCliRunner, Result  # noqa
from typer.main import Typer, get_command as _get_command


class CliRunner(ClickCliRunner):
    def invoke(  # type: ignore
        self,
        app: Typer,
        cli: Typer,
        args: Optional[Union[str, Iterable[str]]] = None,
        input: Optional[Union[bytes, Text, IO[Any]]] = None,
        env: Optional[Mapping[str, str]] = None,
        catch_exceptions: bool = True,
        color: bool = False,
        mix_stderr: bool = False,
        **extra: Any,
    ) -> Result:
        use_cli = _get_command(app)
        return super().invoke(
            use_cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            color=color,
            mix_stderr=mix_stderr,
            **extra,
        )
