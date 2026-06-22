from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import IO, TYPE_CHECKING, Any

from pydantic import TypeAdapter, ValidationError

from . import adapters
from ._click import Context
from ._click.exceptions import BadParameter, UsageError
from .display import get_error_msg
from .models import OptionInfo, ParameterInfo
from .param_types import (
    ParameterAnnotation,
    _open_cli_file,
    annotation_from_prompt,
    choice_coercion_annotation,
    coerce_cli_choice,
    coerce_cli_path,
    file_coercion_annotation,
    path_uses_coercion,
    resolve_file_mode,
    resolve_path_type,
)

if TYPE_CHECKING:
    from .core import TyperParameter


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
            return self.adapter.validate_python(value)
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
class PathRuntimeParam(RuntimeParam):
    """Coercion for path parameters."""

    path_type: type[Any] | None

    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        return coerce_cli_path(
            value,
            self.parameter_info,
            path_type=self.path_type,
            param=param,
            ctx=ctx,
        )


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


@dataclass(frozen=True)
class ChoiceRuntimeParam(RuntimeParam):
    """Coercion for enum and literal choice parameters."""

    choices: tuple[Any, ...]
    case_sensitive: bool

    def _coerce_value(self, value: Any, param: "TyperParameter", ctx: Context) -> Any:
        try:
            return coerce_cli_choice(
                value,
                choices=self.choices,
                case_sensitive=self.case_sensitive,
                ctx=ctx,
            )
        except ValueError as exc:
            raise BadParameter(str(exc), ctx=ctx, param=param) from exc


def build_runtime_param(
    annotation: ParameterAnnotation,
    parameter_info: ParameterInfo,
) -> RuntimeParam:
    """Build runtime coercion for a callback parameter annotation."""
    args = {
        "annotation": annotation,
        "parameter_info": parameter_info,
    }
    file_annotation = file_coercion_annotation(annotation)
    if file_annotation is not None:
        return FileRuntimeParam(**args, file_annotation=file_annotation)
    if path_uses_coercion(annotation, parameter_info):
        return PathRuntimeParam(
            **args,
            path_type=resolve_path_type(annotation, parameter_info),
        )
    choice = choice_coercion_annotation(annotation, parameter_info)
    if choice is not None:
        choices, case_sensitive = choice
        return ChoiceRuntimeParam(
            **args,
            choices=choices,
            case_sensitive=case_sensitive,
        )
    adapter = adapters.try_build_adapter(annotation, parameter_info)
    if adapter is not None:
        return AdapterRuntimeParam(**args, adapter=adapter)
    return PassThroughRuntimeParam(**args)


def bool_flag_runtime_param() -> RuntimeParam:
    """Build runtime coercion for a standalone boolean flag option."""
    return build_runtime_param(
        annotation=bool,
        parameter_info=OptionInfo(),
    )


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
