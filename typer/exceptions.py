class TyperException(Exception):
    """A Typer-specific exception"""

    exit_code = 1

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

    def format_message(self) -> str:
        return self.message


class Abort(RuntimeError):
    """An internal signalling exception that signals Typer to abort."""


class Exit(RuntimeError):
    """An exception that indicates that the application should exit with some
    status code.
    """

    __slots__ = ("exit_code",)

    def __init__(self, code: int = 0) -> None:
        self.exit_code: int = code
