import os
import stat
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    TypeAlias,
    TypeGuard,
    TypeVar,
    cast,
)

from pydantic import TypeAdapter, ValidationError

from ._click import Context
from ._click._compat import open_stream
from ._click.exceptions import BadParameter
from ._click.shell_completion import CompletionItem
from ._click.types import ParamType
from ._click.utils import LazyFile, format_filename, safecall
from ._typing import get_args, get_origin, is_literal_type, literal_values
from .display import get_error_msg
from .models import (
    AnyType,
    FileBinaryRead,
    FileBinaryWrite,
    FileText,
    FileTextWrite,
    ParameterInfo,
)

if TYPE_CHECKING:
    from .core import TyperParameter

ParamTypeValue = TypeVar("ParamTypeValue")

ParameterAnnotation: TypeAlias = Any


def lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def infer_annotation_from_default(default: Any | None) -> ParameterAnnotation:
    """Infer a normalized annotation from a default value."""
    if default is None:
        return str
    if isinstance(default, tuple) and len(default) > 0:
        if not isinstance(default[0], (tuple, list)):
            return tuple.__class_getitem__(tuple(map(type, default)))
    if isinstance(default, (tuple, list)):
        if not default:
            return str
        item = default[0]
        if isinstance(item, (tuple, list)):
            return tuple.__class_getitem__(tuple(map(type, item)))
        return type(item)
    return type(default)


def annotation_from_prompt(t: Any | None, default: Any | None) -> ParameterAnnotation:
    if t is not None and not isinstance(t, ParamType):
        return t
    return infer_annotation_from_default(default)


def resolve_param_type(
    annotation: ParameterAnnotation,
    parameter_info: ParameterInfo | None = None,
) -> ParamType:
    """Resolve a ParamType for this particular annotation."""
    if isinstance(annotation, ParamType):
        return annotation

    if isinstance(annotation, tuple):
        return TyperTuple(annotation)

    if parameter_info is not None:
        if annotation is int or annotation is float:
            if parameter_info.min is not None or parameter_info.max is not None:
                return TyperRanged(annotation)
        if annotation is datetime:
            f = parameter_info.formats
            formats_tuple = tuple(f) if f is not None else ("%Y-%m-%d",)
            return TyperDatetime(formats=formats_tuple)
        if _needs_typer_path(annotation, parameter_info):
            return TyperPath()
        if lenient_issubclass(annotation, Enum):
            return TyperChoice(list(annotation), parameter_info.case_sensitive)
        if is_literal_type(annotation):
            return TyperChoice(
                literal_values(annotation), parameter_info.case_sensitive
            )
        if lenient_issubclass(annotation, CLI_FILE_TYPES):
            return TyperFile()

    return ParamType()


def cli_param_type(
    *,
    annotation: ParameterAnnotation,
    parameter_info: ParameterInfo,
    is_list: bool,
    is_tuple: bool,
) -> ParamType:
    """Defer the param type"""
    if is_tuple:
        type_args = get_args(annotation)
        return resolve_param_type(tuple(type_args), parameter_info)
    if is_list:
        (element_type,) = get_args(annotation)
        return resolve_param_type(element_type, parameter_info)
    return resolve_param_type(annotation, parameter_info)


# DATETIME #
class TyperDatetime(ParamType):
    def __init__(self, *, formats: tuple[str, ...]) -> None:
        self.formats = formats


# TUPLE #
class TyperTuple(ParamType):
    """Metavar and nargs information for tuple parameters."""

    is_composite = True

    def __init__(self, element_annotations: Sequence[Any]) -> None:
        self.element_annotations: tuple[Any, ...] = tuple(element_annotations)

    @property
    def arity(self) -> int:
        return len(self.element_annotations)


# ENUM #
def normalize_choice_value(
    choice: Any,
    case_sensitive: bool,
    ctx: Context | None,
) -> str:
    normed_value = str(choice.value) if isinstance(choice, Enum) else str(choice)
    if ctx is not None and ctx.token_normalize_func is not None:
        normed_value = ctx.token_normalize_func(normed_value)
    if not case_sensitive:
        normed_value = normed_value.casefold()
    return normed_value


def coerce_cli_choice(
    value: Any,
    *,
    choices: Sequence[Any],
    case_sensitive: bool,
    ctx: Context | None,
) -> Any:
    if any(isinstance(choice, Enum) and value is choice for choice in choices):
        return value
    normalized_mapping = {
        c: normalize_choice_value(c, case_sensitive, ctx) for c in choices
    }
    normed_value = normalize_choice_value(value, case_sensitive, ctx)
    for original, normalized in normalized_mapping.items():
        if normalized == normed_value:
            return original
    choices_str = ", ".join(map(repr, normalized_mapping.values()))
    raise ValueError(f"{value!r} is not one of {choices_str}.")


def choice_coercion_annotation(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> tuple[tuple[Any, ...], bool] | None:
    if lenient_issubclass(annotation, Enum):
        return tuple(annotation), parameter_info.case_sensitive
    if is_literal_type(annotation):
        return literal_values(annotation), parameter_info.case_sensitive
    return None


class TyperChoice(ParamType, Generic[ParamTypeValue]):
    name = "choice"

    def __init__(
        self, choices: Iterable[ParamTypeValue], case_sensitive: bool = True
    ) -> None:
        self.choices: Sequence[ParamTypeValue] = tuple(choices)
        self.case_sensitive = case_sensitive

    def _normalized_mapping(
        self, ctx: Context | None = None
    ) -> Mapping[ParamTypeValue, str]:
        """
        Returns mapping where keys are the original choices and the values are
        the normalized values that are accepted via the command line.
        """
        return {
            choice: normalize_choice_value(choice, self.case_sensitive, ctx)
            for choice in self.choices
        }

    def get_missing_message(self, param: "TyperParameter", ctx: Context | None) -> str:
        """Message shown when no choice is passed."""
        choices = ",\n\t".join(self._normalized_mapping(ctx=ctx).values())
        return f"Choose from:\n\t{choices}"

    def get_invalid_choice_message(self, value: Any, ctx: Context | None) -> str:
        """Get the error message when the given choice is invalid."""
        choices_str = ", ".join(map(repr, self._normalized_mapping(ctx=ctx).values()))
        return f"{value!r} is not one of {choices_str}."

    def _choice_as_str(self, choice: ParamTypeValue) -> str:
        if isinstance(choice, Enum):
            return str(choice.value)
        return str(choice)

    def shell_complete(
        self, ctx: Context, param: "TyperParameter", incomplete: str
    ) -> list[CompletionItem]:
        """Complete choices that start with the incomplete value."""

        str_choices = map(self._choice_as_str, self.choices)

        if self.case_sensitive:
            matched = (c for c in str_choices if c.startswith(incomplete))
        else:
            incomplete = incomplete.lower()
            matched = (c for c in str_choices if c.lower().startswith(incomplete))

        return [CompletionItem(c) for c in matched]


# PATH #
def path_metavar_label(parameter_info: ParameterInfo) -> str:
    if parameter_info.file_okay and not parameter_info.dir_okay:
        return "file"
    if parameter_info.dir_okay and not parameter_info.file_okay:
        return "dir"
    return "path"


class TyperPath(ParamType):
    envvar_list_splitter: ClassVar[str] = os.path.pathsep

    def shell_complete(
        self, ctx: Context, param: "TyperParameter", incomplete: str
    ) -> list[CompletionItem]:
        """Return an empty list so that the autocompletion functionality
        will work properly from the commandline.
        """
        return []


def resolve_path_type(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> type[Any] | None:
    path_type = parameter_info.path_type
    if path_type is None and lenient_issubclass(annotation, Path):
        path_type = annotation
    return path_type


def path_uses_coercion(annotation: Any, parameter_info: ParameterInfo) -> bool:
    return _needs_typer_path(annotation, parameter_info)


def _needs_typer_path(annotation: Any, parameter_info: ParameterInfo) -> bool:
    return (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type is not None
        or parameter_info.resolve_path
    )


def _coerce_path_result(
    value: str | os.PathLike[str],
    path_type: type[Any] | None,
) -> str | bytes | os.PathLike[str]:
    if path_type is not None and not isinstance(value, path_type):
        if path_type is bytes:
            return os.fsencode(value)
        return cast("os.PathLike[str]", path_type(value))
    return value


def coerce_cli_path(
    value: str | os.PathLike[str],
    parameter_info: ParameterInfo,
    *,
    path_type: type[Any] | None,
    param: "TyperParameter | None" = None,
    ctx: Context | None = None,
) -> str | bytes | os.PathLike[str] | Path:
    if path_type is None or path_type is str or path_type is bytes:
        rv: Any = value
    elif isinstance(path_type, type) and issubclass(path_type, Path):
        if isinstance(value, path_type):
            rv = value
        elif isinstance(value, (str, os.PathLike)):
            try:
                rv = TypeAdapter(path_type).validate_python(value)
            except ValidationError as exc:
                raise BadParameter(get_error_msg(exc), ctx=ctx, param=param) from exc
        else:
            rv = value
    else:
        rv = value

    is_dash = (
        parameter_info.file_okay and parameter_info.allow_dash and rv in (b"-", "-")
    )

    if not is_dash:
        if parameter_info.resolve_path:
            rv = os.path.realpath(rv)

        label = path_metavar_label(parameter_info)
        try:
            st = os.stat(rv)
        except OSError:
            if not parameter_info.exists:
                return _coerce_path_result(rv, path_type)
            raise BadParameter(
                f"{label} {format_filename(value)!r} does not exist.",
                ctx=ctx,
                param=param,
            ) from None

        loc = repr(format_filename(value))
        if not parameter_info.file_okay and stat.S_ISREG(st.st_mode):
            raise BadParameter(f"{label} {loc} is a file.", ctx=ctx, param=param)

        if not parameter_info.dir_okay and stat.S_ISDIR(st.st_mode):
            raise BadParameter(f"{label} {loc} is a directory.", ctx=ctx, param=param)

        if parameter_info.readable and not os.access(rv, os.R_OK):
            raise BadParameter(f"{label} {loc} is not readable.", ctx=ctx, param=param)

        if parameter_info.writable and not os.access(rv, os.W_OK):
            raise BadParameter(f"{label} {loc} is not writable.", ctx=ctx, param=param)

    return _coerce_path_result(rv, path_type)


# FILE #
CLI_FILE_TYPES = (FileTextWrite, FileText, FileBinaryRead, FileBinaryWrite)


def is_file_annotation(annotation: Any) -> bool:
    return lenient_issubclass(annotation, CLI_FILE_TYPES)


class TyperFile(ParamType):
    envvar_list_splitter = os.path.pathsep

    def shell_complete(
        self, ctx: Context, param: "TyperParameter", incomplete: str
    ) -> list[CompletionItem]:
        return [CompletionItem(incomplete, type="file")]


def file_coercion_annotation(annotation: Any) -> Any | None:
    """Return the file marker type when this parameter opens files."""
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if args and all(is_file_annotation(arg) for arg in args):
            return args[0]
        return None
    if origin is tuple:
        args = get_args(annotation)
        if args and all(is_file_annotation(arg) for arg in args):
            return args[0]
        return None
    if is_file_annotation(annotation):
        return annotation
    return None


def resolve_file_mode(parameter_info: ParameterInfo, annotation: Any) -> str:
    if parameter_info.mode is not None:
        return parameter_info.mode
    if lenient_issubclass(annotation, FileBinaryWrite):
        return "wb"
    if lenient_issubclass(annotation, FileTextWrite):
        return "w"
    if lenient_issubclass(annotation, FileBinaryRead):
        return "rb"
    return "r"


def _is_file_like(value: Any) -> TypeGuard[IO[Any]]:
    return hasattr(value, "read") or hasattr(value, "write")


def _resolve_file_lazy_flag(
    value: str | os.PathLike[str],
    *,
    mode: str,
    lazy: bool | None,
) -> bool:
    if lazy is not None:
        return lazy
    if os.fspath(value) == "-":
        return False
    if "w" in mode:
        return True
    return False


def _open_cli_file(
    value: str | os.PathLike[str] | IO[Any],
    parameter_info: ParameterInfo,
    *,
    mode: str,
    param: "TyperParameter | None" = None,
    ctx: Context | None = None,
) -> IO[Any]:
    if _is_file_like(value):
        return value

    value = cast("str | os.PathLike[str]", value)

    try:
        lazy = _resolve_file_lazy_flag(
            value,
            mode=mode,
            lazy=parameter_info.lazy,
        )

        if lazy:
            lf = LazyFile(
                value,
                mode,
                parameter_info.encoding,
                parameter_info.errors,
                atomic=parameter_info.atomic,
            )

            if ctx is not None:
                ctx.call_on_close(lf.close_intelligently)

            return cast("IO[Any]", lf)

        f, should_close = open_stream(
            value,
            mode,
            parameter_info.encoding,
            parameter_info.errors,
            atomic=parameter_info.atomic,
        )

        if ctx is not None:
            if should_close:
                ctx.call_on_close(safecall(f.close))
            else:
                ctx.call_on_close(safecall(f.flush))

        return f
    except OSError as exc:  # pragma: no cover
        message = f"'{format_filename(value)}': {exc.strerror}"
        raise BadParameter(message, ctx=ctx, param=param) from exc


# RANGE #
class TyperRanged(ParamType):
    def __init__(self, annotation: type[Any]) -> None:
        self.annotation = annotation
