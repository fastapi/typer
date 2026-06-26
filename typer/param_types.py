import os
import stat
from collections.abc import Sequence
from enum import Enum
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    TypeAlias,
    cast,
)

from pydantic import TypeAdapter, ValidationError

from ._click import Context
from ._click._compat import open_stream
from ._click.exceptions import BadParameter
from ._click.utils import LazyFile, format_filename, safecall
from ._typing import get_args, get_origin, is_literal_type, is_union, literal_values
from .display import get_error_msg
from .models import (
    AnyType,
    FileBinaryRead,
    FileBinaryWrite,
    FileText,
    FileTextWrite,
    NoneType,
    ParameterInfo,
    ParamMeta,
)

if TYPE_CHECKING:
    from .core import TyperParameter

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
    if t is not None:
        return t
    return infer_annotation_from_default(default)


def parse_param_annotation(
    param: ParamMeta, default: Any | None
) -> ParameterAnnotation:
    """Parse the annotation for a callback parameter."""
    if param.annotation is not param.empty:
        main_type = param.annotation
        origin = get_origin(main_type)

        if origin is not None:
            if is_union(origin):
                types = []
                for type_ in get_args(main_type):
                    if type_ is NoneType:
                        continue
                    types.append(type_)
                assert len(types) == 1, "Typer currently doesn't support Union types"
                main_type = types[0]
                origin = get_origin(main_type)

            if lenient_issubclass(origin, list):
                element_type = get_args(main_type)[0]
                assert not get_origin(element_type), (
                    "List types with complex sub-types are not currently supported"
                )
                return main_type
            if lenient_issubclass(origin, tuple):
                type_args = get_args(main_type)
                for type_ in type_args:
                    assert not get_origin(type_), (
                        "Tuple types with complex sub-types are not currently supported"
                    )
                return main_type
            return main_type
        return main_type
    return infer_annotation_from_default(default)


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
    ctx: Context | None = None,
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


def choice_as_str(choice: Any) -> str:
    if isinstance(choice, Enum):
        return str(choice.value)
    return str(choice)


# PATH #
def path_type_name(parameter_info: ParameterInfo) -> str:
    if parameter_info.file_okay and not parameter_info.dir_okay:
        return "file"
    if parameter_info.dir_okay and not parameter_info.file_okay:
        return "dir"
    return "path"


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

        label = path_type_name(parameter_info)
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


def _open_cli_file(
    value: str | os.PathLike[str] | IO[Any],
    parameter_info: ParameterInfo,
    *,
    mode: str,
    param: "TyperParameter | None" = None,
    ctx: Context | None = None,
) -> IO[Any]:
    if hasattr(value, "read") or hasattr(value, "write"):
        return cast("IO[Any]", value)

    if isinstance(value, str):
        path: str | os.PathLike[str] = value
    else:
        path = value

    try:
        lazy = parameter_info.lazy
        if lazy is None:
            if os.fspath(path) == "-":
                lazy = False
            elif "w" in mode:
                lazy = True
            else:
                lazy = False

        if lazy:
            lf = LazyFile(
                path,
                mode,
                parameter_info.encoding,
                parameter_info.errors,
                atomic=parameter_info.atomic,
            )

            if ctx is not None:
                ctx.call_on_close(lf.close_intelligently)

            return cast("IO[Any]", lf)

        f, should_close = open_stream(
            path,
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
        message = f"'{format_filename(path)}': {exc.strerror}"
        raise BadParameter(message, ctx=ctx, param=param) from exc
