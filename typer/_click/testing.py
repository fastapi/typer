import contextlib
import io
import os
import shlex
import sys
from collections.abc import Iterator, Mapping, Sequence
from types import TracebackType
from typing import IO, TYPE_CHECKING, Any, BinaryIO, cast

from . import _compat, formatting, termui, utils
from ._compat import _find_binary_reader
from .core import Command

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer


class EchoingStdin:
    def __init__(self, input: BinaryIO, output: BinaryIO) -> None:
        self._input = input
        self._output = output
        self._paused = False

    def __getattr__(self, x: str) -> Any:
        return getattr(self._input, x)

    def _echo(self, rv: bytes) -> bytes:
        if not self._paused:
            self._output.write(rv)

        return rv

    def read(self, n: int = -1) -> bytes:
        return self._echo(self._input.read(n))

    def read1(self, n: int = -1) -> bytes:
        return self._echo(self._input.read1(n))  # type: ignore

    def readline(self, n: int = -1) -> bytes:
        return self._echo(self._input.readline(n))

    def readlines(self) -> list[bytes]:
        return [self._echo(x) for x in self._input.readlines()]

    def __iter__(self) -> Iterator[bytes]:
        return iter(self._echo(x) for x in self._input)

    def __repr__(self) -> str:
        return repr(self._input)


@contextlib.contextmanager
def _pause_echo(stream: EchoingStdin | None) -> Iterator[None]:
    if stream is None:
        yield
    else:
        stream._paused = True
        yield
        stream._paused = False


class BytesIOCopy(io.BytesIO):
    """Patch ``io.BytesIO`` to let the written stream be copied to another."""

    def __init__(self, copy_to: io.BytesIO) -> None:
        super().__init__()
        self.copy_to = copy_to

    def flush(self) -> None:
        super().flush()
        self.copy_to.flush()

    def write(self, b: "ReadableBuffer") -> int:
        self.copy_to.write(b)
        return super().write(b)


class StreamMixer:
    """Mixes `<stdout>` and `<stderr>` streams.

    The result is available in the ``output`` attribute.
    """

    def __init__(self) -> None:
        self.output: io.BytesIO = io.BytesIO()
        self.stdout: io.BytesIO = BytesIOCopy(copy_to=self.output)
        self.stderr: io.BytesIO = BytesIOCopy(copy_to=self.output)

    def __del__(self) -> None:
        """
        Guarantee that embedded file-like objects are closed in a
        predictable order, protecting against races between
        self.output being closed and other streams being flushed on close
        """
        self.stderr.close()
        self.stdout.close()
        self.output.close()


class _NamedTextIOWrapper(io.TextIOWrapper):
    def __init__(self, buffer: BinaryIO, name: str, mode: str, **kwargs: Any) -> None:
        super().__init__(buffer, **kwargs)
        self._name = name
        self._mode = mode

    @property
    def name(self) -> str:
        return self._name

    @property
    def mode(self) -> str:
        return self._mode


def make_input_stream(input: str | bytes | IO[Any] | None, charset: str) -> BinaryIO:
    # Is already an input stream.
    if hasattr(input, "read"):
        rv = _find_binary_reader(cast("IO[Any]", input))

        if rv is not None:
            return rv

        raise TypeError("Could not find binary reader for input stream.")

    if input is None:
        input = b""
    elif isinstance(input, str):
        input = input.encode(charset)

    return io.BytesIO(input)


class Result:
    """Holds the captured result of an invoked CLI script."""

    def __init__(
        self,
        runner: "CliRunner",
        stdout_bytes: bytes,
        stderr_bytes: bytes,
        output_bytes: bytes,
        return_value: Any,
        exit_code: int,
        exception: BaseException | None,
        exc_info: tuple[type[BaseException], BaseException, TracebackType]
        | None = None,
    ):
        self.runner = runner
        self.stdout_bytes = stdout_bytes
        self.stderr_bytes = stderr_bytes
        self.output_bytes = output_bytes
        self.return_value = return_value
        self.exit_code = exit_code
        self.exception = exception
        self.exc_info = exc_info

    @property
    def output(self) -> str:
        """The terminal output as unicode string, as the user would see it."""
        return self.output_bytes.decode(self.runner.charset, "replace").replace(
            "\r\n", "\n"
        )

    @property
    def stdout(self) -> str:
        """The standard output as unicode string."""
        return self.stdout_bytes.decode(self.runner.charset, "replace").replace(
            "\r\n", "\n"
        )

    @property
    def stderr(self) -> str:
        """The standard error as unicode string."""
        return self.stderr_bytes.decode(self.runner.charset, "replace").replace(
            "\r\n", "\n"
        )

    def __repr__(self) -> str:
        exc_str = repr(self.exception) if self.exception else "okay"
        return f"<{type(self).__name__} {exc_str}>"


class CliRunner:
    """The CLI runner provides functionality to invoke a Click command line
    script for unittesting purposes in a isolated environment.  This only
    works in single-threaded systems without any concurrency as it changes the
    global interpreter state.
    """

    def __init__(
        self,
        charset: str = "utf-8",
        env: Mapping[str, str | None] | None = None,
        echo_stdin: bool = False,
        catch_exceptions: bool = True,
    ) -> None:
        self.charset = charset
        self.env: Mapping[str, str | None] = env or {}
        self.echo_stdin = echo_stdin
        self.catch_exceptions = catch_exceptions

    def get_default_prog_name(self, cli: Command) -> str:
        """Given a command object it will return the default program name
        for it.  The default is the `name` attribute or ``"root"`` if not
        set.
        """
        return cli.name or "root"

    def make_env(
        self, overrides: Mapping[str, str | None] | None = None
    ) -> Mapping[str, str | None]:
        """Returns the environment overrides for invoking a script."""
        rv = dict(self.env)
        if overrides:
            rv.update(overrides)
        return rv

    @contextlib.contextmanager
    def isolation(
        self,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        color: bool = False,
    ) -> Iterator[tuple[io.BytesIO, io.BytesIO, io.BytesIO]]:
        """A context manager that sets up the isolation for invoking of a
        command line tool.  This sets up `<stdin>` with the given input data
        and `os.environ` with the overrides from the given dictionary.
        This also rebinds some internals in Click to be mocked (like the
        prompt functionality).
        """
        bytes_input = make_input_stream(input, self.charset)
        echo_input = None

        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_forced_width = formatting.FORCED_WIDTH
        formatting.FORCED_WIDTH = 80

        env = self.make_env(env)

        stream_mixer = StreamMixer()

        if self.echo_stdin:
            bytes_input = echo_input = cast(
                BinaryIO, EchoingStdin(bytes_input, stream_mixer.stdout)
            )

        sys.stdin = text_input = _NamedTextIOWrapper(
            bytes_input, encoding=self.charset, name="<stdin>", mode="r"
        )

        if self.echo_stdin:
            # Force unbuffered reads, otherwise TextIOWrapper reads a
            # large chunk which is echoed early.
            text_input._CHUNK_SIZE = 1  # type: ignore

        sys.stdout = _NamedTextIOWrapper(
            stream_mixer.stdout, encoding=self.charset, name="<stdout>", mode="w"
        )

        sys.stderr = _NamedTextIOWrapper(
            stream_mixer.stderr,
            encoding=self.charset,
            name="<stderr>",
            mode="w",
            errors="backslashreplace",
        )

        @_pause_echo(echo_input)  # type: ignore
        def visible_input(prompt: str | None = None) -> str:
            sys.stdout.write(prompt or "")
            try:
                val = next(text_input).rstrip("\r\n")
            except StopIteration as e:
                raise EOFError() from e
            sys.stdout.write(f"{val}\n")
            sys.stdout.flush()
            return val

        @_pause_echo(echo_input)  # type: ignore
        def hidden_input(prompt: str | None = None) -> str:
            sys.stdout.write(f"{prompt or ''}\n")
            sys.stdout.flush()
            try:
                return next(text_input).rstrip("\r\n")
            except StopIteration as e:
                raise EOFError() from e

        @_pause_echo(echo_input)  # type: ignore
        def _getchar(echo: bool) -> str:
            char = sys.stdin.read(1)

            if echo:
                sys.stdout.write(char)

            sys.stdout.flush()
            return char

        default_color = color

        def should_strip_ansi(
            stream: IO[Any] | None = None, color: bool | None = None
        ) -> bool:
            if color is None:
                return not default_color
            return not color

        old_visible_prompt_func = termui.visible_prompt_func
        old_hidden_prompt_func = termui.hidden_prompt_func
        old__getchar_func = termui._getchar
        old_should_strip_ansi = utils.should_strip_ansi  # type: ignore
        old__compat_should_strip_ansi = _compat.should_strip_ansi
        termui.visible_prompt_func = visible_input
        termui.hidden_prompt_func = hidden_input
        termui._getchar = _getchar
        utils.should_strip_ansi = should_strip_ansi  # type: ignore
        _compat.should_strip_ansi = should_strip_ansi

        old_env = {}
        try:
            for key, value in env.items():
                old_env[key] = os.environ.get(key)
                if value is None:
                    try:
                        del os.environ[key]
                    except Exception:
                        pass
                else:
                    os.environ[key] = value
            yield (stream_mixer.stdout, stream_mixer.stderr, stream_mixer.output)
        finally:
            for key, value in old_env.items():
                if value is None:
                    try:
                        del os.environ[key]
                    except Exception:
                        pass
                else:
                    os.environ[key] = value
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.stdin = old_stdin
            termui.visible_prompt_func = old_visible_prompt_func
            termui.hidden_prompt_func = old_hidden_prompt_func
            termui._getchar = old__getchar_func
            utils.should_strip_ansi = old_should_strip_ansi  # type: ignore
            _compat.should_strip_ansi = old__compat_should_strip_ansi
            formatting.FORCED_WIDTH = old_forced_width

    def invoke(
        self,
        cli: Command,
        args: str | Sequence[str] | None = None,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        catch_exceptions: bool | None = None,
        color: bool = False,
        **extra: Any,
    ) -> Result:
        """Invokes a command in an isolated environment.  The arguments are
        forwarded directly to the command line script, the `extra` keyword
        arguments are passed to the `Command.main` function of
        the command.
        """
        exc_info = None
        if catch_exceptions is None:
            catch_exceptions = self.catch_exceptions

        with self.isolation(input=input, env=env, color=color) as outstreams:
            return_value = None
            exception: BaseException | None = None
            exit_code = 0

            if isinstance(args, str):
                args = shlex.split(args)

            try:
                prog_name = extra.pop("prog_name")
            except KeyError:
                prog_name = self.get_default_prog_name(cli)

            try:
                return_value = cli.main(args=args or (), prog_name=prog_name, **extra)
            except SystemExit as e:
                exc_info = sys.exc_info()
                e_code = cast("int | Any | None", e.code)

                if e_code is None:
                    e_code = 0

                if e_code != 0:
                    exception = e

                if not isinstance(e_code, int):
                    sys.stdout.write(str(e_code))
                    sys.stdout.write("\n")
                    e_code = 1

                exit_code = e_code

            except Exception as e:
                if not catch_exceptions:
                    raise
                exception = e
                exit_code = 1
                exc_info = sys.exc_info()
            finally:
                sys.stdout.flush()
                sys.stderr.flush()
                stdout = outstreams[0].getvalue()
                stderr = outstreams[1].getvalue()
                output = outstreams[2].getvalue()

        return Result(
            runner=self,
            stdout_bytes=stdout,
            stderr_bytes=stderr,
            output_bytes=output,
            return_value=return_value,
            exit_code=exit_code,
            exception=exception,
            exc_info=exc_info,  # type: ignore
        )
