from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID as UUIDType

from ._click import types
from ._types import TyperChoice
from ._typing import is_literal_type, literal_values
from .models import (
    AnyType,
    FileBinaryRead,
    FileBinaryWrite,
    FileText,
    FileTextWrite,
    ParameterInfo,
    TyperPath,
)


def lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def _file_param_type(parameter_info: ParameterInfo, *, mode: str) -> types.File:
    return types.File(
        mode=parameter_info.mode or mode,
        encoding=parameter_info.encoding,
        errors=parameter_info.errors,
        lazy=parameter_info.lazy,
        atomic=parameter_info.atomic,
    )


def _ranged_number_param_type(
    number_class: type[Any],
    *,
    min: int | float | None,
    max: int | float | None,
    clamp: bool,
) -> types.ParamType:
    return types.PydanticParamType(
        types.build_type_adapter(number_class, min=min, max=max, clamp=clamp),
        name="integer range" if number_class is int else "float range",
    )


def _needs_typer_path(annotation: Any, parameter_info: ParameterInfo) -> bool:
    return (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type is not None
        or parameter_info.resolve_path
    )


def get_param_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> types.ParamType:
    if parameter_info.parser is not None:
        return types.FuncParamType(parameter_info.parser)

    param_type = param_type_from_annotation(annotation, parameter_info)
    if param_type is not None:
        return param_type

    raise RuntimeError(f"Type not yet supported: {annotation}")  # pragma: no cover


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
        return types.INT if annotation is int else types.FLOAT
    if annotation is UUIDType:
        return types.UUID
    if annotation is datetime:
        return types.datetime_param_type(formats=parameter_info.formats)
    if annotation is bool:
        return types.BOOL
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
        return types.STRING
    if lenient_issubclass(annotation, FileTextWrite):
        return _file_param_type(parameter_info, mode="w")
    if lenient_issubclass(annotation, FileText):
        return _file_param_type(parameter_info, mode="r")
    if lenient_issubclass(annotation, FileBinaryRead):
        return _file_param_type(parameter_info, mode="rb")
    if lenient_issubclass(annotation, FileBinaryWrite):
        return _file_param_type(parameter_info, mode="wb")
    return None
