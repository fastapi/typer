from collections.abc import Sequence
from typing import IO, TYPE_CHECKING, Any, Union

from ._compat import get_text_stderr
from .globals import resolve_color_default
from .utils import echo, format_filename

if TYPE_CHECKING:
    from .core import Command, Context, Parameter


def _join_param_hints(param_hint: Sequence[str] | str | None) -> str | None:
    if param_hint is not None and not isinstance(param_hint, str):
        return " / ".join(repr(x) for x in param_hint)

    return param_hint


class ClickException(Exception):
    """An exception that Click can handle and show to the user."""

    exit_code = 1

    def __init__(self, message: str) -> None:
        super().__init__(message)
        # The context will be removed by the time we print the message, so cache
        # the color settings here to be used later on (in `show`)
        self.show_color: bool | None = resolve_color_default()
        self.message = message

    def format_message(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message

    def show(self, file: IO[Any] | None = None) -> None:
        if file is None:
            file = get_text_stderr()

        echo(
            f"Error: {self.format_message()}",
            file=file,
            color=self.show_color,
        )


class UsageError(ClickException):
    """An internal exception that signals a usage error.  This typically
    aborts any further handling.
    """

    exit_code = 2

    def __init__(self, message: str, ctx: Union["Context", None] = None) -> None:
        super().__init__(message)
        self.ctx = ctx
        self.cmd: Command | None = self.ctx.command if self.ctx else None

    def show(self, file: IO[Any] | None = None) -> None:
        if file is None:
            file = get_text_stderr()
        color = None
        hint = ""
        if (
            self.ctx is not None
            and self.ctx.command.get_help_option(self.ctx) is not None
        ):
            command = self.ctx.command_path
            option = self.ctx.help_option_names[0]
            hint = f"Try '{command} {option}' for help.\n"
        if self.ctx is not None:
            color = self.ctx.color
            echo(f"{self.ctx.get_usage()}\n{hint}", file=file, color=color)
        echo(
            f"Error: {self.format_message()}",
            file=file,
            color=color,
        )


class BadParameter(UsageError):
    """An exception that formats out a standardized error message for a
    bad parameter.  This is useful when thrown from a callback or type as
    Click will attach contextual information to it (for instance, which
    parameter it is).
    """

    def __init__(
        self,
        message: str,
        ctx: Union["Context", None] = None,
        param: Union["Parameter", None] = None,
        param_hint: Sequence[str] | str | None = None,
    ) -> None:
        super().__init__(message, ctx)
        self.param = param
        self.param_hint = param_hint

    def format_message(self) -> str:
        if self.param_hint is not None:
            param_hint = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.ctx)  # type: ignore
        else:
            return f"Invalid value: {self.message}"

        hint = _join_param_hints(param_hint)
        return f"Invalid value for {hint}: {self.message}"


class MissingParameter(BadParameter):
    """Raised if click required an option or argument but it was not
    provided when invoking the script.
    """

    def __init__(
        self,
        message: str | None = None,
        ctx: Union["Context", None] = None,
        param: Union["Parameter", None] = None,
        param_hint: Sequence[str] | str | None = None,
        param_type: str | None = None,
    ) -> None:
        super().__init__(message or "", ctx, param, param_hint)
        self.param_type = param_type

    def format_message(self) -> str:
        if self.param_hint is not None:
            param_hint: Sequence[str] | str | None = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.ctx)  # type: ignore
        else:
            param_hint = None

        param_hint = _join_param_hints(param_hint)
        param_hint = f" {param_hint}" if param_hint else ""

        param_type = self.param_type
        if param_type is None and self.param is not None:
            param_type = self.param.param_type_name

        msg = self.message
        if self.param is not None:
            msg_extra = self.param.type.get_missing_message(
                param=self.param, ctx=self.ctx
            )
            if msg_extra:
                if msg:
                    msg += f". {msg_extra}"
                else:
                    msg = msg_extra

        msg = f" {msg}" if msg else ""

        # Translate param_type for known types.
        if param_type == "argument":
            missing = "Missing argument"
        elif param_type == "option":
            missing = "Missing option"
        elif param_type == "parameter":
            missing = "Missing parameter"
        else:
            missing = f"Missing {param_type}"

        return f"{missing}{param_hint}.{msg}"

    def __str__(self) -> str:
        if not self.message:
            param_name = self.param.name if self.param else None
            return f"Missing parameter: {param_name}"
        else:
            return self.message


class NoSuchOption(UsageError):
    """Raised if click attempted to handle an option that does not
    exist.
    """

    def __init__(
        self,
        option_name: str,
        message: str | None = None,
        possibilities: Sequence[str] | None = None,
        ctx: Union["Context", None] = None,
    ) -> None:
        if message is None:
            message = f"No such option: {option_name}"

        super().__init__(message, ctx)
        self.option_name = option_name
        self.possibilities = possibilities

    def format_message(self) -> str:
        if not self.possibilities:
            return self.message

        possibility_str = ", ".join(sorted(self.possibilities))
        suggest = (f"(Possible options: {possibility_str})",)
        return f"{self.message} {suggest}"


class BadOptionUsage(UsageError):
    """Raised if an option is generally supplied but the use of the option
    was incorrect.  This is for instance raised if the number of arguments
    for an option is not correct.
    """

    def __init__(
        self, option_name: str, message: str, ctx: Union["Context", None] = None
    ) -> None:
        super().__init__(message, ctx)
        self.option_name = option_name


class BadArgumentUsage(UsageError):
    """Raised if an argument is generally supplied but the use of the argument
    was incorrect.  This is for instance raised if the number of values
    for an argument is not correct.
    """


class NoArgsIsHelpError(UsageError):
    def __init__(self, ctx: "Context") -> None:
        self.ctx: Context
        super().__init__(ctx.get_help(), ctx=ctx)

    def show(self, file: IO[Any] | None = None) -> None:
        echo(self.format_message(), file=file, err=True, color=self.ctx.color)


class FileError(ClickException):
    """Raised if a file cannot be opened."""

    def __init__(self, filename: str, hint: str | None = None) -> None:
        if hint is None:
            hint = "unknown error"

        super().__init__(hint)
        self.ui_filename: str = format_filename(filename)
        self.filename = filename

    def format_message(self) -> str:
        return f"Could not open file {self.ui_filename!r}: {self.message}"


class Abort(RuntimeError):
    """An internal signalling exception that signals Click to abort."""


class Exit(RuntimeError):
    """An exception that indicates that the application should exit with some
    status code.
    """

    __slots__ = ("exit_code",)

    def __init__(self, code: int = 0) -> None:
        self.exit_code: int = code
