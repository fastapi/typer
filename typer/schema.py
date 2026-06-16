from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import IO, TYPE_CHECKING, Any

from pydantic import TypeAdapter, ValidationError

from . import adapters
from ._click import Context
from ._click.exceptions import BadParameter, UsageError
from ._click.types import ParamType
from ._typing import get_args, get_origin, is_union
from .models import (
    ArgumentInfo,
    NoneType,
    OptionInfo,
    ParameterInfo,
    ParamMeta,
    Required,
)

if TYPE_CHECKING:
    from .core import TyperParameter
from .param_types import (
    _get_error_msg,
    _open_cli_file,
    choice_coercion_annotation,
    coerce_cli_choice,
    coerce_cli_path,
    file_coercion_annotation,
    infer_type_from_default,
    lenient_issubclass,
    path_uses_coercion,
    resolve_file_mode,
    resolve_path_type,
)


@dataclass(frozen=True)
class DeclaredParam:
    """Parameter metadata declared on a Typer command callback."""

    name: str
    parameter_info: ParameterInfo
    default: Any
    required: bool
    annotation: Any


@dataclass(frozen=True)
class RuntimeParam(ABC):
    """Runtime coercion contract for one command parameter."""

    name: str
    parameter_info: ParameterInfo
    annotation: Any

    def coerce(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
        is_multi_value = param.multiple or param.nargs == -1
        if value is None:
            if is_multi_value:
                return ()
            return None
        if is_multi_value and isinstance(value, str):
            raise BadParameter("Value must be an iterable.", ctx=ctx, param=param)
        return self._coerce_value(value, param=param, ctx=ctx)

    @abstractmethod
    def _coerce_value(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
        pass


@dataclass(frozen=True)
class AdapterRuntimeParam(RuntimeParam):
    """Coercion via a Pydantic TypeAdapter."""

    adapter: TypeAdapter[Any]

    def _coerce_value(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
        try:
            return self.adapter.validate_python(value)
        except ValidationError as exc:
            raise BadParameter(_get_error_msg(exc), ctx=ctx, param=param) from exc
        except ValueError as exc:
            raise BadParameter(str(exc), ctx=ctx, param=param) from exc


@dataclass(frozen=True)
class FileRuntimeParam(RuntimeParam):
    """Coercion by opening CLI file paths into IO streams."""

    file_annotation: Any

    def _coerce_value(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
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

    def _coerce_value(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
        return coerce_cli_path(
            value,
            self.parameter_info,
            path_type=self.path_type,
            param=param,
            ctx=ctx,
        )


@dataclass(frozen=True)
class ChoiceRuntimeParam(RuntimeParam):
    """Coercion for enum and literal choice parameters."""

    choices: tuple[Any, ...]
    case_sensitive: bool

    def _coerce_value(
        self,
        value: Any,
        *,
        param: TyperParameter,
        ctx: Context,
    ) -> Any:
        try:
            return coerce_cli_choice(
                value,
                choices=self.choices,
                case_sensitive=self.case_sensitive,
                ctx=ctx,
            )
        except ValueError as exc:
            raise BadParameter(str(exc), ctx=ctx, param=param) from exc


@dataclass(frozen=True)
class CommandSchema:
    """Schema for all parameters on a Typer command."""

    params: tuple[RuntimeParam, ...]

    @classmethod
    def from_params(cls, command_params: Sequence[Any]) -> CommandSchema:
        runtime_params = [
            param.runtime_param
            for param in command_params
            if getattr(param, "runtime_param", None) is not None
        ]
        return cls(params=tuple(runtime_params))

    def get_param(self, name: str) -> RuntimeParam | None:
        for runtime_param in self.params:
            if runtime_param.name == name:
                return runtime_param
        return None


def declare_param(param: ParamMeta) -> DeclaredParam:
    """Declare metadata from a function parameter."""
    default = None
    required = False
    if isinstance(param.default, ParameterInfo):
        parameter_info = param.default
        if parameter_info.default == Required:
            required = True
        else:
            default = parameter_info.default
    elif param.default == Required or param.default is param.empty:
        required = True
        parameter_info = ArgumentInfo()
    else:
        default = param.default
        parameter_info = OptionInfo()

    pydantic_annotation: Any

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
                assert len(types) == 1, "Typer Currently doesn't support Union types"
                main_type = types[0]
                origin = get_origin(main_type)

            if lenient_issubclass(origin, list):
                element_type = get_args(main_type)[0]
                assert not get_origin(element_type), (
                    "List types with complex sub-types are not currently supported"
                )
                pydantic_annotation = main_type
            elif lenient_issubclass(origin, tuple):
                type_args = get_args(main_type)
                for type_ in type_args:
                    assert not get_origin(type_), (
                        "Tuple types with complex sub-types are not currently supported"
                    )
                pydantic_annotation = main_type
            else:
                pydantic_annotation = main_type
        else:
            pydantic_annotation = main_type
    else:
        if default is not None:
            main_type, guessed = infer_type_from_default(default)
            if main_type is None:
                main_type = str
            elif (
                guessed
                and isinstance(main_type, tuple)
                and all(isinstance(item, type) for item in main_type)
            ):
                main_type = tuple.__class_getitem__(main_type)
            elif guessed and main_type not in (int, float, bool, str):
                main_type = str
        else:
            main_type = str
        pydantic_annotation = main_type

    return DeclaredParam(
        name=param.name,
        parameter_info=parameter_info,
        default=default,
        required=required,
        annotation=pydantic_annotation,
    )


def _runtime_param_fields(declared: DeclaredParam) -> dict[str, Any]:
    return {
        "name": declared.name,
        "annotation": declared.annotation,
        "parameter_info": declared.parameter_info,
    }


def bool_flag_runtime_param(*, name: str, default: bool = False) -> RuntimeParam:
    """Build runtime coercion for a standalone boolean flag option."""
    declared = DeclaredParam(
        name=name,
        parameter_info=OptionInfo(),
        default=default,
        required=False,
        annotation=bool,
    )
    return runtime_param_from_declared(declared)


def prompt_value_proc(
    type: Any | None = None,
    default: Any | None = None,
) -> Callable[[Any], Any]:
    """Coerce interactive prompt input via the runtime adapter layer."""
    annotation = type
    if isinstance(annotation, ParamType):
        annotation = None
    if annotation is None and default is not None:
        annotation, _ = infer_type_from_default(default)
    if annotation is None:
        annotation = str

    parameter_info = OptionInfo()
    adapter = adapters.build_adapter(annotation, parameter_info)

    def coerce(value: Any) -> Any:
        try:
            return adapter.validate_python(value)
        except ValidationError as exc:
            raise UsageError(_get_error_msg(exc)) from exc
        except ValueError as exc:
            raise UsageError(str(exc)) from exc

    return coerce


def runtime_param_from_declared(declared: DeclaredParam) -> RuntimeParam:
    common = _runtime_param_fields(declared)
    file_annotation = file_coercion_annotation(declared.annotation)
    if file_annotation is not None:
        return FileRuntimeParam(**common, file_annotation=file_annotation)
    if path_uses_coercion(declared.annotation, declared.parameter_info):
        return PathRuntimeParam(
            **common,
            path_type=resolve_path_type(declared.annotation, declared.parameter_info),
        )
    choice = choice_coercion_annotation(declared.annotation, declared.parameter_info)
    if choice is not None:
        choices, case_sensitive = choice
        return ChoiceRuntimeParam(
            **common,
            choices=choices,
            case_sensitive=case_sensitive,
        )
    return AdapterRuntimeParam(
        **common,
        adapter=adapters.build_adapter(declared.annotation, declared.parameter_info),
    )
