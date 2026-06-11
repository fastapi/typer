import os
import sys
from collections.abc import Callable, Sequence
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    ClassVar,
    NoReturn,
    TypedDict,
    TypeGuard,
    Union,
    cast,
)

from ._compat import _get_argv_encoding, open_stream
from .exceptions import BadParameter
from .utils import LazyFile, format_filename, safecall

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


class FuncParamType(ParamType):
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.name: str = getattr(func, "__name__", "function")
        self.func = func

    def convert(
        self, value: Any, param: Union["Parameter", None], ctx: Union["Context", None]
    ) -> Any:
        try:
            return self.func(value)
        except ValueError:
            try:
                value = str(value)
            except UnicodeError:  # pragma: no cover
                assert isinstance(value, bytes)
                value = value.decode("utf-8", "replace")

            self.fail(value, param, ctx)


class StringParamType(ParamType):
    name = "text"

    def convert(
        self, value: Any, param: Union["Parameter", None], ctx: Union["Context", None]
    ) -> Any:
        if isinstance(value, bytes):
            enc = _get_argv_encoding()
            try:
                value = value.decode(enc)
            except UnicodeError:
                fs_enc = sys.getfilesystemencoding()
                if fs_enc != enc:
                    try:
                        value = value.decode(fs_enc)
                    except UnicodeError:
                        value = value.decode("utf-8", "replace")
                else:
                    value = value.decode("utf-8", "replace")
            return value
        return str(value)

    def __repr__(self) -> str:
        return "STRING"


class File(ParamType):
    """Declares a parameter to be a file for reading or writing.  The file
    is automatically closed once the context tears down (after the command
    finished working).

    Files can be opened for reading or writing.  The special value ``-``
    indicates stdin or stdout depending on the mode.

    By default, the file is opened for reading text data, but it can also be
    opened in binary mode or for writing.  The encoding parameter can be used
    to force a specific encoding.

    The `lazy` flag controls if the file should be opened immediately or upon
    first IO. The default is to be non-lazy for standard input and output
    streams as well as files opened for reading, `lazy` otherwise. When opening a
    file lazily for reading, it is still opened temporarily for validation, but
    will not be held open until first IO. lazy is mainly useful when opening
    for writing to avoid creating the file until it is needed.

    Files can also be opened atomically in which case all writes go into a
    separate file in the same folder and upon completion the file will
    be moved over to the original location.  This is useful if a file
    regularly read by other users is modified.
    """

    name = "filename"
    envvar_list_splitter: ClassVar[str] = os.path.pathsep

    def __init__(
        self,
        mode: str = "r",
        encoding: str | None = None,
        errors: str | None = "strict",
        lazy: bool | None = None,
        atomic: bool = False,
    ) -> None:
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.lazy = lazy
        self.atomic = atomic

    def resolve_lazy_flag(self, value: str | os.PathLike[str]) -> bool:
        if self.lazy is not None:
            return self.lazy
        if os.fspath(value) == "-":
            return False
        elif "w" in self.mode:
            return True
        return False

    def convert(
        self,
        value: str | os.PathLike[str] | IO[Any],
        param: Union["Parameter", None],
        ctx: Union["Context", None],
    ) -> IO[Any]:
        if _is_file_like(value):
            return value

        value = cast("str | os.PathLike[str]", value)

        try:
            lazy = self.resolve_lazy_flag(value)

            if lazy:
                lf = LazyFile(
                    value, self.mode, self.encoding, self.errors, atomic=self.atomic
                )

                if ctx is not None:
                    ctx.call_on_close(lf.close_intelligently)

                return cast("IO[Any]", lf)

            f, should_close = open_stream(
                value, self.mode, self.encoding, self.errors, atomic=self.atomic
            )

            # If a context is provided, we automatically close the file
            # at the end of the context execution (or flush out).  If a
            # context does not exist, it's the caller's responsibility to
            # properly close the file.  This for instance happens when the
            # type is used with prompts.
            if ctx is not None:
                if should_close:
                    ctx.call_on_close(safecall(f.close))
                else:
                    ctx.call_on_close(safecall(f.flush))

            return f
        except OSError as e:  # pragma: no cover
            self.fail(f"'{format_filename(value)}': {e.strerror}", param, ctx)

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> list["CompletionItem"]:
        """Return a special completion marker that tells the completion
        system to use the shell to provide file path completions.
        """
        from .shell_completion import CompletionItem

        return [CompletionItem(incomplete, type="file")]


def _is_file_like(value: Any) -> TypeGuard[IO[Any]]:
    return hasattr(value, "read") or hasattr(value, "write")


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
        self.types: Sequence[ParamType] = [convert_type(ty) for ty in types]

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


def convert_type(ty: Any | None, default: Any | None = None) -> ParamType:
    """Find the most appropriate `ParamType` for the given Python
    type. If the type isn't provided, it can be inferred from a default
    value.
    """
    from .. import param_types

    guessed_type = False

    if ty is None and default is not None:
        if isinstance(default, (tuple, list)):
            # If the default is empty, ty will remain None and will
            # return STRING.
            if default:
                item = default[0]

                # A tuple of tuples needs to detect the inner types.
                # Can't call convert recursively because that would
                # incorrectly unwind the tuple to a single type.
                if isinstance(item, (tuple, list)):
                    ty = tuple(map(type, item))
                else:
                    ty = type(item)
        else:
            ty = type(default)

        guessed_type = True

    if isinstance(ty, tuple):
        return Tuple(ty)

    if isinstance(ty, ParamType):
        return ty

    if ty is str or ty is None:
        return STRING

    if ty is int:
        return param_types.INT

    if ty is float:
        return param_types.FLOAT

    if ty is bool:
        return param_types.BOOL

    if guessed_type:
        return STRING

    return FuncParamType(ty)


# A unicode string parameter type which is the implicit default.  This
# can also be selected by using ``str`` as type.
STRING = StringParamType()


class OptionHelpExtra(TypedDict, total=False):
    envvars: tuple[str, ...]
    default: str
    range: str
    required: str
