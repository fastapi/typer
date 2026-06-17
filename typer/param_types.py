import os
import stat
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, ClassVar, Generic, TypeGuard, TypeVar, cast

from pydantic import TypeAdapter, ValidationError

from ._click import Context
from ._click._compat import open_stream
from ._click.exceptions import BadParameter
from ._click.shell_completion import CompletionItem
from ._click.types import ParamType
from ._click.utils import LazyFile, format_filename, safecall
from ._typing import get_args, get_origin, is_literal_type, literal_values
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
DEFAULT_PARAM_TYPE = ParamType()


def lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def _get_error_msg(exc: ValidationError) -> str:
    """Get a string representation of the (first) validation error."""
    errors = exc.errors()
    if errors:
        return errors[0]["msg"]
    return str(exc)


def _format_option_metavar(param: "TyperParameter", value_metavar: str) -> str:
    if param.nargs != 1:
        value_metavar += "..."
    return value_metavar


def _format_argument_metavar(param: "TyperParameter", value_metavar: str | None) -> str:
    var = (param.name or "").upper()
    if not param.required:
        var = f"[{var}]"
    if value_metavar:
        var += f":{value_metavar}"
    if param.nargs != 1:
        var += "..."
    return var


def resolve_metavar(param: "TyperParameter", ctx: Context) -> str:
    if param.metavar is not None:
        var = param.metavar
        if getattr(param, "param_type_name", None) == "argument":
            if not param.required and not var.startswith("["):
                var = f"[{var}]"
        return var

    value_metavar = resolve_value_metavar(param, ctx)
    if getattr(param, "param_type_name", None) == "argument":
        return _format_argument_metavar(param, value_metavar)
    assert value_metavar is not None
    return _format_option_metavar(param, value_metavar)


def resolve_value_metavar(param: "TyperParameter", ctx: Context) -> str | None:
    param_type = param.type
    if isinstance(param_type, TyperChoice):
        return choice_value_metavar(
            param,
            ctx,
            choices=param_type.choices,
            case_sensitive=param_type.case_sensitive,
        )
    if getattr(param, "param_type_name", None) == "argument" and not isinstance(
        param_type, TyperDatetime
    ):
        return None
    return param_type_metavar_label(param)


def resolve_rich_metavar(param: "TyperParameter", ctx: Context) -> str | None:
    metavar_str = resolve_metavar(param, ctx)
    if (
        getattr(param, "param_type_name", None) == "argument"
        and param.name
        and metavar_str == param.name.upper()
    ):
        metavar_str = param_type_metavar_label(param)
    if metavar_str == "BOOL":
        return None
    return metavar_str


def _annotation_metavar_label(annotation: Any) -> str:
    display_type = str(annotation)
    origin = get_origin(annotation)
    if annotation is None:
        display_type = "str"
    elif origin is list:
        args = get_args(annotation)
        if len(args) == 1:
            element_label = _annotation_metavar_label(args[0])
            display_type = f"list[{element_label}]"
        else:
            display_type = "list"
    elif origin is tuple:
        labels = [_annotation_metavar_label(arg) for arg in get_args(annotation)]
        display_type = ",".join(labels)
    elif isinstance(annotation, type):
        display_type = annotation.__name__
    return display_type


def param_type_metavar_label(param: "TyperParameter") -> str:
    annotation = param.runtime_param.annotation
    param_type = param.type
    if get_origin(annotation) is list:
        label = _annotation_metavar_label(annotation)
    elif isinstance(param_type, TyperDatetime):
        label = "|".join(param_type.formats)
    elif isinstance(param_type, TyperRanged):
        label = f"{param_type.annotation.__name__} range"
    elif isinstance(param_type, TyperTuple):
        labels = [
            _annotation_metavar_label(element)
            for element in param_type.element_annotations
        ]
        label = ",".join(labels)
    elif isinstance(param_type, TyperPath):
        label = path_metavar_label(param.runtime_param.parameter_info)
    else:
        label = _annotation_metavar_label(param.runtime_param.annotation)
    return f"<{label}>"


def infer_type_from_default(default: Any) -> tuple[Any | None, bool]:
    """Infer a type from a default value. Returns (annotation, guessed)."""
    if isinstance(default, tuple) and default:
        if not isinstance(default[0], (tuple, list)):
            return tuple(map(type, default)), True
    if isinstance(default, (tuple, list)):
        if not default:
            return None, True
        item = default[0]
        if isinstance(item, (tuple, list)):
            return tuple(map(type, item)), True
        return type(item), True
    return type(default), True


def resolve_param_type(
    annotation: Any | None = None,
    default: Any | None = None,
    *,
    parameter_info: ParameterInfo | None = None,
) -> ParamType:
    """Resolve a display ParamType for metavar/help."""
    if annotation is None and default is not None:
        annotation, _ = infer_type_from_default(default)

    if isinstance(annotation, tuple):
        return TyperTuple(annotation)

    if isinstance(annotation, ParamType):
        return annotation

    if parameter_info is not None and annotation is not None:
        param_type = param_type_from_annotation(annotation, parameter_info)
        if param_type is not None:
            return param_type

    return DEFAULT_PARAM_TYPE


def cli_param_type(
    *,
    annotation: Any,
    parameter_info: ParameterInfo,
    default: Any,
    is_list: bool,
    is_tuple: bool,
) -> ParamType:
    """Defer the "type" for metavar/help."""
    if is_tuple:
        type_args = get_args(annotation)
        return resolve_param_type(tuple(type_args), parameter_info=parameter_info)
    if is_list:
        (element_type,) = get_args(annotation)
        return resolve_param_type(element_type, parameter_info=parameter_info)
    return resolve_param_type(
        annotation, default=default, parameter_info=parameter_info
    )


def get_param_type(*, annotation: Any, parameter_info: ParameterInfo) -> ParamType:
    return resolve_param_type(annotation=annotation, parameter_info=parameter_info)


def param_type_from_annotation(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> ParamType | None:
    if annotation is int or annotation is float:
        if parameter_info.min is not None or parameter_info.max is not None:
            return TyperRanged(annotation)
        return None
    if annotation is datetime:
        f = parameter_info.formats
        formats_tuple = tuple(f) if f is not None else ("%Y-%m-%d",)
        return TyperDatetime(formats=formats_tuple)
    if _needs_typer_path(annotation, parameter_info):
        return TyperPath()
    if lenient_issubclass(annotation, Enum):
        return TyperChoice(list(annotation), parameter_info.case_sensitive)
    if is_literal_type(annotation):
        return TyperChoice(literal_values(annotation), parameter_info.case_sensitive)
    if lenient_issubclass(annotation, CLI_FILE_TYPES):
        return TyperFile()
    return None


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


def choice_value_metavar(
    param: "TyperParameter",
    ctx: Context,
    *,
    choices: Sequence[Any],
    case_sensitive: bool,
) -> str:
    if param.param_type_name == "option" and not param.show_choices:  # type: ignore
        metavars = [_annotation_metavar_label(type(c)) for c in choices]
        choices_str = "|".join([*dict.fromkeys(metavars)])
    else:
        normalized_mapping = {
            c: normalize_choice_value(c, case_sensitive, ctx) for c in choices
        }
        choices_str = "|".join(normalized_mapping.values())

    if param.required and param.param_type_name == "argument":
        return f"{{{choices_str}}}"

    return f"[{choices_str}]"


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
                raise BadParameter(_get_error_msg(exc), ctx=ctx, param=param) from exc
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
