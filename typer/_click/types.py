from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    NoReturn,
    Union,
)

from .exceptions import BadParameter

if TYPE_CHECKING:
    from .core import Context, Parameter
    from .shell_completion import CompletionItem


class ParamType:
    """Represents the type of a parameter. Validates and converts values
    from the command line or Python into the correct type.

    To implement a custom type, subclass and implement at least the
    following:

    -   The `name` class attribute must be set.
    -   Calling an instance of the type with ``None`` must return
        ``None``. This is already implemented by default.
    -   `convert` must convert string values to the correct type.
    -   `convert` must accept values that are already the correct
        type.
    -   It must be able to convert a value if the ``ctx`` and ``param``
        arguments are ``None``. This can occur when converting prompt
        input.
    """

    is_composite: ClassVar[bool] = False
    arity: ClassVar[int] = 1
    name: str

    # if a list of this type is expected and the value is pulled from a
    # string environment variable, this is what splits it up.  `None`
    # means any whitespace.  For all parameters the general rule is that
    # whitespace splits them up.  The exception are paths and files which
    # are split by ``os.path.pathsep`` by default (":" on Unix and ";" on
    # Windows).
    envvar_list_splitter: ClassVar[str | None] = None

    def __call__(
        self,
        value: Any,
        param: Union["Parameter", None] = None,
        ctx: Union["Context", None] = None,
    ) -> Any:
        if value is not None:
            return self.convert(value, param, ctx)

    def get_metavar(self, param: "Parameter", ctx: "Context") -> str | None:
        """Returns the metavar default for this param if it provides one."""
        pass  # pragma: no cover

    def get_missing_message(
        self, param: "Parameter", ctx: Union["Context", None]
    ) -> str | None:
        """Optionally might return extra information about a missing
        parameter.
        """
        pass  # pragma: no cover

    def convert(
        self, value: Any, param: Union["Parameter", None], ctx: Union["Context", None]
    ) -> Any:
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


class CompositeParamType(ParamType):
    is_composite = True

    @property
    def arity(self) -> int:  # type: ignore
        raise NotImplementedError()  # pragma: no cover


class Tuple(CompositeParamType):
    """The default behavior of Click is to apply a type on a value directly.
    This works well in most cases, except for when `nargs` is set to a fixed
    count and different types should be used for different items.  In this
    case the `Tuple` type can be used.  This type can only be used
    if `nargs` is set to a fixed number.

    For more information see `tuple-type`.

    This can be selected by using a Python tuple literal as a type.
    """

    def __init__(self, types: Sequence[type[Any] | ParamType]) -> None:
        from ..param_types import resolve_param_type

        self.types: Sequence[ParamType] = [
            item if isinstance(item, ParamType) else resolve_param_type(item)
            for item in types
        ]

    @property
    def name(self) -> str:  # type: ignore[override]
        return f"<{' '.join(ty.name for ty in self.types)}>"

    @property
    def arity(self) -> int:  # type: ignore
        return len(self.types)

    def convert(
        self, value: Any, param: Union["Parameter", None], ctx: Union["Context", None]
    ) -> Any:
        len_type = len(self.types)
        len_value = len(value)

        if len_value != len_type:
            self.fail(
                f"{len_type} values are required, but {len_value} given.",
                param=param,
                ctx=ctx,
            )

        return tuple(
            ty(x, param, ctx) for ty, x in zip(self.types, value, strict=False)
        )
