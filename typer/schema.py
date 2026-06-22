from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import IO, TYPE_CHECKING, Any

from pydantic import TypeAdapter, ValidationError

from . import adapters
from ._click import Context
from ._click.exceptions import BadParameter, UsageError
from ._typing import get_args, get_origin, is_union
from .display import get_error_msg
from .models import (
    ArgumentInfo,
    NoneType,
    OptionInfo,
    ParameterInfo,
    ParamMeta,
    Required,
)
from .param_types import (
    ParameterAnnotation,
    _open_cli_file,
    annotation_from_prompt,
    choice_coercion_annotation,
    coerce_cli_choice,
    coerce_cli_path,
    file_coercion_annotation,
    infer_annotation_from_default,
    lenient_issubclass,
    path_uses_coercion,
    resolve_file_mode,
    resolve_path_type,
)

if TYPE_CHECKING:
    from .core import TyperParameter


@dataclass(frozen=True)
class DeclaredParam:
    """Parameter metadata declared on a Typer command callback."""

    name: str
    parameter_info: ParameterInfo
    default: Any
    required: bool
    annotation: ParameterAnnotation


@dataclass(frozen=True)
class RuntimeParam(ABC):
    """Runtime coercion contract for one command parameter."""

    name: str
    parameter_info: ParameterInfo
    annotation: ParameterAnnotation

    def coerce(
        self,
        value: Any,
        *,
        param: "TyperParameter",
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

    pydantic_annotation: ParameterAnnotation

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
        pydantic_annotation = infer_annotation_from_default(default)

    return DeclaredParam(
        name=param.name,
        parameter_info=parameter_info,
        default=default,
        required=required,
        annotation=pydantic_annotation,
    )


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


def runtime_param_from_declared(declared: DeclaredParam) -> RuntimeParam:
    args = {
        "name": declared.name,
        "annotation": declared.annotation,
        "parameter_info": declared.parameter_info,
    }
    file_annotation = file_coercion_annotation(declared.annotation)
    if file_annotation is not None:
        return FileRuntimeParam(**args, file_annotation=file_annotation)
    if path_uses_coercion(declared.annotation, declared.parameter_info):
        return PathRuntimeParam(
            **args,
            path_type=resolve_path_type(declared.annotation, declared.parameter_info),
        )
    choice = choice_coercion_annotation(declared.annotation, declared.parameter_info)
    if choice is not None:
        choices, case_sensitive = choice
        return ChoiceRuntimeParam(
            **args,
            choices=choices,
            case_sensitive=case_sensitive,
        )
    adapter = adapters.try_build_adapter(declared.annotation, declared.parameter_info)
    if adapter is not None:
        return AdapterRuntimeParam(**args, adapter=adapter)
    return PassThroughRuntimeParam(**args)
