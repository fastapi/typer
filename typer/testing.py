from collections.abc import Mapping, Sequence
from typing import IO, Any, Optional, Union

from click.testing import CliRunner as ClickCliRunner  # noqa
from click.testing import Result
from typer.main import Typer
from typer.main import get_command as _get_command


class CliRunner(ClickCliRunner):
    def invoke(  # type: ignore
        self,
        app: Typer,
        args: Optional[Union[str, Sequence[str]]] = None,
        input: Optional[Union[bytes, str, IO[Any]]] = None,
        env: Optional[Mapping[str, Optional[str]]] = None,
        catch_exceptions: bool = True,
        color: bool = False,
        **extra: Any,
    ) -> Result:
        """Invokes a Typer application in an isolated environment.

        This is a Typer-specific wrapper around Click's CliRunner.invoke() method.
        The arguments are forwarded directly to the command line script, the `extra`
        keyword arguments are passed to the :meth:`~click.Command.main` function of
        the command.

        This returns a :class:`click.testing.Result` object.

        :param app: the Typer application to invoke
        :param args: the arguments to invoke. It may be given as an iterable
                     or a string. When given as string it will be interpreted
                     as a Unix shell command. More details at
                     :func:`shlex.split`.
        :param input: the input data for `sys.stdin`.
        :param env: the environment overrides.
        :param catch_exceptions: Whether to catch any other exceptions than
                                 ``SystemExit``.
        :param color: whether the output should contain color codes. The
                      application can still override this explicitly.
        :param extra: the keyword arguments to pass to :meth:`main`.
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
