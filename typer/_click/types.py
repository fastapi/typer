from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    ClassVar,
    NoReturn,
    Union,
)

from .exceptions import BadParameter

if TYPE_CHECKING:
    from .core import Context, Parameter
    from .shell_completion import CompletionItem


class ParamType:
    """Display and plumbing metadata for a CLI parameter type."""

    is_composite: ClassVar[bool] = False

    @property
    def arity(self) -> int:
        return 1

    # if a list of this type is expected and the value is pulled from a
    # string environment variable, this is what splits it up.  `None`
    # means any whitespace.  For all parameters the general rule is that
    # whitespace splits them up.  The exception are paths and files which
    # are split by ``os.path.pathsep`` by default (":" on Unix and ";" on
    # Windows).
    envvar_list_splitter: ClassVar[str | None] = None

    def get_missing_message(
        self, param: "Parameter", ctx: Union["Context", None]
    ) -> str | None:
        """Optionally might return extra information about a missing
        parameter.
        """
        pass  # pragma: no cover

    def split_envvar_value(self, rv: str) -> Sequence[str]:
        """Given a value from an environment variable this splits it up
        into small chunks depending on the defined envvar list splitter.

        If the splitter is set to `None`, which means that whitespace splits,
        then leading and trailing whitespace is ignored.  Otherwise, leading
        and trailing splitters usually lead to empty items being included.
        """
        return (rv or "").split(self.envvar_list_splitter)

    def fail(
        self,
        message: str,
        param: Union["Parameter", None] = None,
        ctx: Union["Context", None] = None,
    ) -> NoReturn:
        """Helper method to fail with an invalid value message."""
        raise BadParameter(message, ctx=ctx, param=param)

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> list["CompletionItem"]:
        """Return a list of `CompletionItem` objects for the
        incomplete value. Most types do not provide completions, but
        some do, and this allows custom types to provide custom
        completions as well.
        """
        return []
