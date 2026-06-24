import os
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any

from pydantic import TypeAdapter, ValidationError

from . import adapters
from ._click import Context
from ._click.exceptions import BadParameter, UsageError
from ._typing import get_args, get_origin, is_number_type
from .adapters import validation_context
from .display import get_error_msg
from .models import OptionInfo, ParameterInfo
from .param_types import (
    ParameterAnnotation,
    _open_cli_file,
    annotation_from_prompt,
    choice_coercion_annotation,
    file_coercion_annotation,
    is_file_annotation,
    lenient_issubclass,
    path_metavar_label,
    resolve_file_mode,
)

if TYPE_CHECKING:
    from .core import TyperParameter


@dataclass(frozen=True)
class TypeDescriptor:
    """Resolved CLI type: metadata, coercion adapter, and deduced flags."""

    annotation: ParameterAnnotation
    parameter_info: ParameterInfo
    adapter: TypeAdapter[Any] | None
    file_annotation: Any | None

    @property
    def is_list(self) -> bool:
        return lenient_issubclass(get_origin(self.annotation), list)

    @property
    def is_tuple(self) -> bool:
        return lenient_issubclass(get_origin(self.annotation), tuple)

    @property
    def is_datetime(self) -> bool:
        return self.annotation is datetime

    @property
    def is_ranged(self) -> bool:
        if self.is_list or self.is_tuple:
            return False
        return is_number_type(self.annotation) and (
            self.parameter_info.min is not None or self.parameter_info.max is not None
        )

    @property
    def is_path(self) -> bool:
        return self.annotation is Path

    @property
    def is_choice(self) -> bool:
        return self.choices is not None

    @property
    def is_file(self) -> bool:
        return self.file_annotation is not None

    @property
    def datetime_formats(self) -> tuple[str, ...]:
        formats = self.parameter_info.formats
        if formats is not None:
            return tuple(formats)
        return ("%Y-%m-%d",)

    @property
    def path_label(self) -> str:
        return path_metavar_label(self.parameter_info)

    @property
    def choices(self) -> tuple[Any, ...] | None:
        if self.is_list:
            args = get_args(self.annotation)
            if len(args) == 1:
                choice = choice_coercion_annotation(args[0], self.parameter_info)
                if choice is not None:
                    return choice[0]
        choice = choice_coercion_annotation(self.annotation, self.parameter_info)
        if choice is not None:
            return choice[0]
        return None

    @property
    def case_sensitive(self) -> bool:
        return self.parameter_info.case_sensitive

    @property
    def ranged_type_name(self) -> str:
        if isinstance(self.annotation, type):
            return self.annotation.__name__
        return "number"

    @property
    def tuple_arity(self) -> int | None:
        if not self.is_tuple:
            return None
        return len(get_args(self.annotation))

    @property
    def envvar_list_splitter(self) -> str | None:
        if self.is_file:
            return os.path.pathsep
        if self.is_path:
            return os.path.pathsep
        if self.is_list:
            args = get_args(self.annotation)
            if len(args) == 1 and (is_file_annotation(args[0]) or args[0] is Path):
                return os.path.pathsep
        return None


def resolve_type_descriptor(
    annotation: ParameterAnnotation,
    parameter_info: ParameterInfo,
) -> TypeDescriptor:
    """Resolve Pydantic adapter for one parameter annotation."""
    file_annotation = file_coercion_annotation(annotation)
    adapter = None
    if file_annotation is None:
        adapter = adapters.try_build_adapter(annotation, parameter_info)
    return TypeDescriptor(
        annotation=annotation,
        parameter_info=parameter_info,
        adapter=adapter,
        file_annotation=file_annotation,
    )


@dataclass(frozen=True)
class RuntimeParam(ABC):
    """Runtime coercion contract for one command parameter."""

    parameter_info: ParameterInfo
    annotation: ParameterAnnotation

    def coerce(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        is_multi_value = param.multiple or param.nargs == -1
        if value is None:
            if is_multi_value:
                return ()
            return None
        if is_multi_value and isinstance(value, str):
            raise BadParameter("Value must be an iterable.", ctx=ctx, param=param)
        return self._coerce_value(value, param=param, ctx=ctx)

    @abstractmethod
    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        pass


@dataclass(frozen=True)
class AdapterRuntimeParam(RuntimeParam):
    """Coercion via a Pydantic TypeAdapter."""

    adapter: TypeAdapter[Any]

    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        try:
            return self.adapter.validate_python(
                value,
                context=validation_context(ctx, param),
            )
        except ValidationError as exc:
            raise BadParameter(get_error_msg(exc), ctx=ctx, param=param) from exc
        except ValueError as exc:
            raise BadParameter(str(exc), ctx=ctx, param=param) from exc


@dataclass(frozen=True)
class FileRuntimeParam(RuntimeParam):
    """Coercion by opening CLI file paths into IO streams."""

    file_annotation: Any

    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        mode = resolve_file_mode(self.parameter_info, self.file_annotation)

        def open_one(item: Any) -> IO[Any]:
            return _open_cli_file(
                item,
                self.parameter_info,
                mode=mode,
                param=param,
                ctx=ctx,
            )

        if isinstance(value, (list, tuple)):
            return type(value)(open_one(item) for item in value)
        return open_one(value)


@dataclass(frozen=True)
class PassThroughRuntimeParam(RuntimeParam):
    """Coercion for annotations that cannot use a Pydantic TypeAdapter."""

    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        annotation = self.annotation
        if isinstance(annotation, type):
            if isinstance(value, annotation):
                return value
        label = getattr(annotation, "__name__", repr(annotation))
        raise BadParameter(
            f"Value {value!r} is not a valid {label}.",
            ctx=ctx,
            param=param,
        )


def build_runtime_param(descriptor: TypeDescriptor) -> RuntimeParam:
    """Build runtime coercion from a resolved type descriptor."""
    args = {
        "annotation": descriptor.annotation,
        "parameter_info": descriptor.parameter_info,
    }
    if descriptor.file_annotation is not None:
        return FileRuntimeParam(**args, file_annotation=descriptor.file_annotation)
    if descriptor.adapter is not None:
        return AdapterRuntimeParam(**args, adapter=descriptor.adapter)
    return PassThroughRuntimeParam(**args)


def bool_flag_type_descriptor() -> TypeDescriptor:
    """Resolved type for a standalone boolean flag option."""
    return resolve_type_descriptor(
        annotation=bool,
        parameter_info=OptionInfo(),
    )


def bool_flag_runtime_param() -> RuntimeParam:
    """Build runtime coercion for a standalone boolean flag option."""
    return build_runtime_param(bool_flag_type_descriptor())


def prompt_value_proc(
    param_type: Any | None = None,
    default: Any | None = None,
) -> Callable[[Any], Any]:
    """Coerce interactive prompt input via the runtime adapter layer."""
    annotation = annotation_from_prompt(param_type, default)

    parameter_info = OptionInfo()
    adapter = adapters.try_build_adapter(annotation, parameter_info)

    if adapter is not None:

        def coerce(value: Any) -> Any:
            try:
                return adapter.validate_python(value)
            except ValidationError as exc:
                raise UsageError(get_error_msg(exc)) from exc
            except ValueError as exc:
                raise UsageError(str(exc)) from exc

        return coerce

    def coerce_pass_through(value: Any) -> Any:
        if isinstance(annotation, type):
            if isinstance(value, annotation):
                return value
        label = getattr(annotation, "__name__", repr(annotation))
        raise UsageError(f"Value {value!r} is not a valid {label}.")

    return coerce_pass_through
