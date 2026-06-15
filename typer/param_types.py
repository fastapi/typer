import os
import stat
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import IO, Annotated, Any, ClassVar, Generic, TypeGuard, TypeVar, cast
from uuid import UUID as UUIDType

from pydantic import BeforeValidator, TypeAdapter, ValidationError

from ._click import Context, Parameter, types
from ._click._compat import open_stream
from ._click.exceptions import BadParameter
from ._click.shell_completion import CompletionItem
from ._click.utils import LazyFile, format_filename, safecall
from ._typing import get_args as typer_get_args
from ._typing import get_origin as typer_get_origin
from ._typing import is_literal_type, literal_values
from .models import (
    AnyType,
    FileBinaryRead,
    FileBinaryWrite,
    FileText,
    FileTextWrite,
    ParameterInfo,
)

ParamTypeValue = TypeVar("ParamTypeValue")


def lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def _get_error_msg(exc: ValidationError) -> str:
    """Get a string representation of the (first) validation error."""
    errors = exc.errors()
    if errors:
        return errors[0]["msg"]
    return str(exc)


class DisplayParamType(types.ParamType):
    """Used for metavar/help only."""

    def __init__(
        self,
        *,
        name: str,
        repr_name: str | None = None,
        metavar: str | Callable[[Parameter, Context], str | None] | None = None,
    ) -> None:
        self.name = name
        self._repr_name = repr_name or name
        self._metavar = metavar

    def convert(
        self,
        value: Any,
        param: Parameter | None,
        ctx: Context | None,
    ) -> Any:
        return value

    def get_metavar(self, param: Parameter, ctx: Context) -> str | None:
        if self._metavar is None:
            return None
        if isinstance(self._metavar, str):
            return self._metavar
        return self._metavar(param, ctx)

    def __repr__(self) -> str:
        return self._repr_name


def datetime_param_type(formats: Sequence[str] | None = None) -> DisplayParamType:
    formats_tuple = tuple(formats) if formats is not None else None
    metavar_formats = formats_tuple or ["%Y-%m-%d"]

    return DisplayParamType(
        name="datetime",
        repr_name="DateTime",
        metavar=f"[{'|'.join(metavar_formats)}]",
    )


INT = DisplayParamType(name="integer", repr_name="INT")

FLOAT = DisplayParamType(name="float", repr_name="FLOAT")

BOOL = DisplayParamType(name="boolean", repr_name="BOOL")

UUID = DisplayParamType(name="uuid", repr_name="UUID")

STRING = DisplayParamType(name="text", repr_name="STRING")


class FileDisplayType(DisplayParamType):
    envvar_list_splitter = os.path.pathsep

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> list[CompletionItem]:
        return [CompletionItem(incomplete, type="file")]


FILE = FileDisplayType(name="filename", repr_name="File")

CLI_FILE_TYPES = (FileTextWrite, FileText, FileBinaryRead, FileBinaryWrite)


class TyperTuple(types.ParamType):
    """Metavar and nargs information for tuple parameters."""

    is_composite = True

    def __init__(self, element_types: Sequence[types.ParamType]) -> None:
        self.types: tuple[types.ParamType, ...] = tuple(element_types)
        self.name = f"<{' '.join(t.name for t in self.types)}>"

    @property
    def arity(self) -> int:
        return len(self.types)

    def convert(
        self,
        value: Any,
        param: Parameter | None,
        ctx: Context | None,
    ) -> Any:
        len_type = len(self.types)
        len_value = len(value)
        if len_value != len_type:
            self.fail(
                f"{len_type} values are required, but {len_value} given.",
                param=param,
                ctx=ctx,
            )
        return value


class TyperChoice(types.ParamType, Generic[ParamTypeValue]):
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
            choice: self.normalize_choice(
                choice=choice,
                ctx=ctx,
            )
            for choice in self.choices
        }

    def normalize_choice(self, choice: ParamTypeValue, ctx: Context | None) -> str:
        normed_value = str(choice.value) if isinstance(choice, Enum) else str(choice)

        if ctx is not None and ctx.token_normalize_func is not None:
            normed_value = ctx.token_normalize_func(normed_value)

        if not self.case_sensitive:
            normed_value = normed_value.casefold()

        return normed_value

    def get_metavar(self, param: Parameter, ctx: Context) -> str | None:
        if param.param_type_name == "option" and not param.show_choices:  # type: ignore
            choice_metavars = [
                resolve_param_type(type(choice)).name.upper() for choice in self.choices
            ]
            choices_str = "|".join([*dict.fromkeys(choice_metavars)])
        else:
            choices_str = "|".join(
                [str(i) for i in self._normalized_mapping(ctx=ctx).values()]
            )

        # Use curly braces to indicate a required argument.
        if param.required and param.param_type_name == "argument":
            return f"{{{choices_str}}}"

        # Use square braces to indicate an option or optional argument.
        return f"[{choices_str}]"

    def get_missing_message(self, param: Parameter, ctx: Context | None) -> str:
        """Message shown when no choice is passed."""
        choices = ",\n\t".join(self._normalized_mapping(ctx=ctx).values())
        return f"Choose from:\n\t{choices}"

    def _build_class_adapter(self, ctx: Context | None) -> TypeAdapter[ParamTypeValue]:
        normalized_mapping = self._normalized_mapping(ctx=ctx)

        def parse_choice(value: Any) -> ParamTypeValue:
            normed_value = self.normalize_choice(choice=value, ctx=ctx)
            for original, normalized in normalized_mapping.items():
                if normalized == normed_value:
                    return original
            raise ValueError(self.get_invalid_choice_message(value=value, ctx=ctx))

        return TypeAdapter(Annotated[Any, BeforeValidator(parse_choice)])

    def convert(
        self, value: Any, param: Parameter | None, ctx: Context | None
    ) -> ParamTypeValue:
        try:
            return self._build_class_adapter(ctx).validate_python(value)
        except ValidationError as exc:
            self.fail(_get_error_msg(exc), param=param, ctx=ctx)

    def get_invalid_choice_message(self, value: Any, ctx: Context | None) -> str:
        """Get the error message when the given choice is invalid."""
        choices_str = ", ".join(map(repr, self._normalized_mapping(ctx=ctx).values()))
        return f"{value!r} is not one of {choices_str}."

    def __repr__(self) -> str:
        return f"Choice({list(self.choices)})"

    def _choice_as_str(self, choice: ParamTypeValue) -> str:
        if isinstance(choice, Enum):
            return str(choice.value)
        return str(choice)

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> list[CompletionItem]:
        """Complete choices that start with the incomplete value."""

        str_choices = map(self._choice_as_str, self.choices)

        if self.case_sensitive:
            matched = (c for c in str_choices if c.startswith(incomplete))
        else:
            incomplete = incomplete.lower()
            matched = (c for c in str_choices if c.lower().startswith(incomplete))

        return [CompletionItem(c) for c in matched]


class TyperPath(types.ParamType):
    envvar_list_splitter: ClassVar[str] = os.path.pathsep

    def __init__(
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: type[Any] | None = None,
    ):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.readable = readable
        self.writable = writable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = "file"
        elif self.dir_okay and not self.file_okay:
            self.name = "directory"
        else:
            self.name = "path"

    def _parse_path_value(
        self,
        value: Any,
        param: Parameter | None,
        ctx: Context | None,
    ) -> Any:
        if self.type is None or self.type is str or self.type is bytes:
            return value
        if isinstance(self.type, type) and issubclass(self.type, Path):
            if isinstance(value, self.type):
                return value
            if isinstance(value, (str, os.PathLike)):
                try:
                    return TypeAdapter(self.type).validate_python(value)
                except ValidationError as exc:
                    self.fail(_get_error_msg(exc), param, ctx)
        return value

    def coerce_path_result(
        self, value: str | os.PathLike[str]
    ) -> str | bytes | os.PathLike[str]:
        if self.type is not None and not isinstance(value, self.type):
            if (
                self.type is str
            ):  # pragma: no cover  # TODO: perhaps this branch can't be hit and should be removed
                return os.fsdecode(value)
            elif self.type is bytes:
                return os.fsencode(value)
            else:
                return cast("os.PathLike[str]", self.type(value))

        return value

    def convert(
        self,
        value: str | os.PathLike[str],
        param: Parameter | None,
        ctx: Context | None,
    ) -> str | bytes | os.PathLike[str]:
        rv = self._parse_path_value(value, param, ctx)

        is_dash = self.file_okay and self.allow_dash and rv in (b"-", "-")

        if not is_dash:
            if self.resolve_path:
                rv = os.path.realpath(rv)

            try:
                st = os.stat(rv)
            except OSError:
                if not self.exists:
                    return self.coerce_path_result(rv)
                self.fail(
                    f"{self.name.title()} {format_filename(value)!r} does not exist.",
                    param,
                    ctx,
                )

            name = self.name.title()
            loc = repr(format_filename(value))
            if not self.file_okay and stat.S_ISREG(st.st_mode):
                self.fail(f"{name} {loc} is a file.", param, ctx)

            if not self.dir_okay and stat.S_ISDIR(st.st_mode):
                self.fail(f"{name} {loc} is a directory.", param, ctx)

            if self.readable and not os.access(rv, os.R_OK):
                self.fail(f"{name} {loc} is not readable.", param, ctx)

            if self.writable and not os.access(rv, os.W_OK):
                self.fail(f"{name} {loc} is not writable.", param, ctx)

        return self.coerce_path_result(rv)

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> list[CompletionItem]:
        """Return an empty list so that the autocompletion functionality
        will work properly from the commandline.
        """
        return []


def is_file_annotation(annotation: Any) -> bool:
    return lenient_issubclass(annotation, CLI_FILE_TYPES)


def file_coercion_annotation(annotation: Any) -> Any | None:
    """Return the file marker type when this parameter opens files."""
    origin = typer_get_origin(annotation)
    if origin is list:
        args = typer_get_args(annotation)
        if args and all(is_file_annotation(arg) for arg in args):
            return args[0]
        return None
    if origin is tuple:
        args = typer_get_args(annotation)
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
    param: Parameter | None = None,
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


def _file_param_type() -> FileDisplayType:
    return FILE


def _ranged_number_param_type(
    number_class: type[Any],
    *,
    min: int | float | None,
    max: int | float | None,
    clamp: bool,
) -> types.ParamType:
    return DisplayParamType(
        name="integer range" if number_class is int else "float range",
    )


def _needs_typer_path(annotation: Any, parameter_info: ParameterInfo) -> bool:
    return (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type is not None
        or parameter_info.resolve_path
    )


def infer_type_from_default(default: Any) -> tuple[Any | None, bool]:
    """Infer a type from a default value. Returns (annotation, guessed)."""
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
) -> types.ParamType:
    """Resolve a display ``ParamType`` for metavar/help."""
    guessed_type = False
    if annotation is None and default is not None:
        annotation, guessed_type = infer_type_from_default(default)

    if isinstance(annotation, tuple):
        element_types: list[types.ParamType] = []
        for element in annotation:
            if isinstance(element, types.ParamType):
                element_types.append(element)
            else:
                element_types.append(
                    resolve_param_type(
                        annotation=element, parameter_info=parameter_info
                    )
                )
        return TyperTuple(element_types)

    if isinstance(annotation, types.ParamType):
        return annotation

    if parameter_info is not None and annotation is not None:
        param_type = param_type_from_annotation(annotation, parameter_info)
        if param_type is not None:
            return param_type

    if annotation is str or annotation is None:
        return STRING
    if annotation is int:
        return INT
    if annotation is float:
        return FLOAT
    if annotation is bool:
        return BOOL

    if guessed_type:
        return STRING

    return STRING


def cli_param_type(
    *,
    annotation: Any,
    parameter_info: ParameterInfo,
    default: Any,
    is_list: bool,
    is_tuple: bool,
) -> types.ParamType:
    """Defer the "type" for metavar/help."""
    if is_tuple:
        type_args = typer_get_args(annotation)
        return resolve_param_type(tuple(type_args), parameter_info=parameter_info)
    if is_list:
        (element_type,) = typer_get_args(annotation)
        return resolve_param_type(element_type, parameter_info=parameter_info)
    return resolve_param_type(
        annotation, default=default, parameter_info=parameter_info
    )


def get_param_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> types.ParamType:
    return resolve_param_type(annotation=annotation, parameter_info=parameter_info)


def param_type_from_annotation(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> types.ParamType | None:
    if annotation is int or annotation is float:
        if parameter_info.min is not None or parameter_info.max is not None:
            min_ = parameter_info.min
            max_ = parameter_info.max
            if annotation is int:
                min_ = int(min_) if min_ is not None else None
                max_ = int(max_) if max_ is not None else None
            return _ranged_number_param_type(
                annotation,
                min=min_,
                max=max_,
                clamp=parameter_info.clamp,
            )
        return INT if annotation is int else FLOAT
    if annotation is UUIDType:
        return UUID
    if annotation is datetime:
        return datetime_param_type(formats=parameter_info.formats)
    if annotation is bool:
        return BOOL
    if _needs_typer_path(annotation, parameter_info):
        resolved_path_type: type[Any] | None = parameter_info.path_type
        if resolved_path_type is None and lenient_issubclass(annotation, Path):
            resolved_path_type = annotation
        return TyperPath(
            exists=parameter_info.exists,
            file_okay=parameter_info.file_okay,
            dir_okay=parameter_info.dir_okay,
            writable=parameter_info.writable,
            readable=parameter_info.readable,
            resolve_path=parameter_info.resolve_path,
            allow_dash=parameter_info.allow_dash,
            path_type=resolved_path_type,
        )
    if lenient_issubclass(annotation, Enum):
        return TyperChoice(
            list(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if is_literal_type(annotation):
        return TyperChoice(
            literal_values(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if annotation is str:
        return STRING
    if lenient_issubclass(annotation, CLI_FILE_TYPES):
        return _file_param_type()
    return None
