from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import IO, Any, Literal

from pydantic import TypeAdapter, ValidationError

from . import adapters
from ._click.exceptions import BadParameter
from ._typing import get_args as typer_get_args
from ._typing import get_origin as typer_get_origin
from ._typing import is_union
from .models import (
    ArgumentInfo,
    NoneType,
    OptionInfo,
    ParameterInfo,
    ParamMeta,
    Required,
)
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

ParamKind = Literal["option", "argument"]


@dataclass(frozen=True)
class DeclaredParam:
    """Parameter metadata declared on a Typer command callback."""

    name: str
    parameter_info: ParameterInfo
    default: Any
    required: bool
    annotation: Any
    is_list: bool
    is_tuple: bool
    is_flag: bool | None


@dataclass(frozen=True)
class RuntimeParam(ABC):
    """Runtime coercion contract for one command parameter."""

    name: str
    parameter_info: ParameterInfo
    default: Any
    required: bool
    annotation: Any
    kind: ParamKind
    multiple: bool
    nargs: int
    is_flag: bool
    is_bool_flag: bool

    def coerce(
        self,
        value: Any,
        *,
        param: Any | None = None,
        ctx: Any | None = None,
    ) -> Any:
        if value is None:
            return None
        return self._coerce_value(value, param=param, ctx=ctx)

    @abstractmethod
    def _coerce_value(
        self,
        value: Any,
        *,
        param: Any | None,
        ctx: Any | None,
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
        param: Any | None,
        ctx: Any | None,
    ) -> Any:
        try:
            return self.adapter.validate_python(value)
        except ValidationError as exc:
            if param is None:
                raise

            raise BadParameter(_get_error_msg(exc), ctx=ctx, param=param) from exc
        except ValueError as exc:
            if param is None:
                raise

            raise BadParameter(str(exc), ctx=ctx, param=param) from exc


@dataclass(frozen=True)
class FileRuntimeParam(RuntimeParam):
    """Coercion by opening CLI file paths into IO streams."""

    file_annotation: Any

    def _coerce_value(
        self,
        value: Any,
        *,
        param: Any | None,
        ctx: Any | None,
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
        param: Any | None,
        ctx: Any | None,
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
        param: Any | None,
        ctx: Any | None,
    ) -> Any:
        try:
            return coerce_cli_choice(
                value,
                choices=self.choices,
                case_sensitive=self.case_sensitive,
                ctx=ctx,
            )
        except ValueError as exc:
            if param is None:
                raise
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

    def coerce(self, values: dict[str, Any]) -> dict[str, Any]:
        coerced: dict[str, Any] = {}
        for name, value in values.items():
            runtime_param = self.get_param(name)
            if runtime_param is not None:
                coerced[name] = runtime_param.coerce(value, param=None, ctx=None)
        return coerced


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

    is_list = False
    is_tuple = False
    is_flag: bool | None = None
    pydantic_annotation: Any

    if param.annotation is not param.empty:
        main_type = param.annotation
        origin = typer_get_origin(main_type)

        if origin is not None:
            if is_union(origin):
                types = []
                for type_ in typer_get_args(main_type):
                    if type_ is NoneType:
                        continue
                    types.append(type_)
                assert len(types) == 1, "Typer Currently doesn't support Union types"
                main_type = types[0]
                origin = typer_get_origin(main_type)

            if lenient_issubclass(origin, list):
                element_type = typer_get_args(main_type)[0]
                assert not typer_get_origin(element_type), (
                    "List types with complex sub-types are not currently supported"
                )
                is_list = True
                pydantic_annotation = main_type
            elif lenient_issubclass(origin, tuple):
                type_args = typer_get_args(main_type)
                for type_ in type_args:
                    assert not typer_get_origin(type_), (
                        "Tuple types with complex sub-types are not currently supported"
                    )
                is_tuple = True
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
            elif guessed and main_type not in (int, float, bool, str):
                main_type = str
        else:
            main_type = str
        pydantic_annotation = main_type

    if isinstance(parameter_info, OptionInfo) and pydantic_annotation is bool:
        is_flag = True
    elif (
        is_list
        and isinstance(parameter_info, OptionInfo)
        and parameter_info.param_decls
        and typer_get_args(pydantic_annotation) == (bool,)
    ):
        for decl in parameter_info.param_decls:
            if "/" in decl:
                is_flag = True
                break

    return DeclaredParam(
        name=param.name,
        parameter_info=parameter_info,
        default=default,
        required=required,
        annotation=pydantic_annotation,
        is_list=is_list,
        is_tuple=is_tuple,
        is_flag=is_flag,
    )


def _runtime_param_fields(
    declared: DeclaredParam,
    *,
    kind: ParamKind,
    multiple: bool,
    nargs: int,
    is_bool_flag: bool,
) -> dict[str, Any]:
    return {
        "name": declared.name,
        "annotation": declared.annotation,
        "parameter_info": declared.parameter_info,
        "kind": kind,
        "multiple": multiple,
        "nargs": nargs,
        "is_flag": bool(declared.is_flag),
        "is_bool_flag": is_bool_flag,
        "required": declared.required,
        "default": declared.default,
    }


def runtime_param_from_declared(
    declared: DeclaredParam,
    *,
    kind: ParamKind,
    multiple: bool,
    nargs: int,
    is_bool_flag: bool,
) -> RuntimeParam:
    common = _runtime_param_fields(
        declared,
        kind=kind,
        multiple=multiple,
        nargs=nargs,
        is_bool_flag=is_bool_flag,
    )
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
