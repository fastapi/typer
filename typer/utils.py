import inspect
from copy import copy
from inspect import Parameter
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    cast,
    get_type_hints,
)

from typing_extensions import Annotated

from ._typing import get_args, get_origin
from .models import ArgumentInfo, OptionInfo, ParameterInfo, ParamMeta

try:
    import pydantic
except ImportError:
    pydantic = None

PYDANTIC_FIELD_DELIMITER = "__"


def _param_type_to_user_string(param_type: Type[ParameterInfo]) -> str:
    # Render a `ParameterInfo` subclass for use in error messages.
    # User code doesn't call `*Info` directly, so errors should present the classes how
    # they were (probably) defined in the user code.
    if param_type is OptionInfo:
        return "`Option`"
    elif param_type is ArgumentInfo:
        return "`Argument`"
    # This line shouldn't be reachable during normal use.
    return f"`{param_type.__name__}`"  # pragma: no cover


class AnnotatedParamWithDefaultValueError(Exception):
    argument_name: str
    param_type: Type[ParameterInfo]

    def __init__(self, argument_name: str, param_type: Type[ParameterInfo]):
        self.argument_name = argument_name
        self.param_type = param_type

    def __str__(self) -> str:
        param_type_str = _param_type_to_user_string(self.param_type)
        return (
            f"{param_type_str} default value cannot be set in `Annotated`"
            f" for {self.argument_name!r}. Set the default value with `=` instead."
        )


class MixedAnnotatedAndDefaultStyleError(Exception):
    argument_name: str
    annotated_param_type: Type[ParameterInfo]
    default_param_type: Type[ParameterInfo]

    def __init__(
        self,
        argument_name: str,
        annotated_param_type: Type[ParameterInfo],
        default_param_type: Type[ParameterInfo],
    ):
        self.argument_name = argument_name
        self.annotated_param_type = annotated_param_type
        self.default_param_type = default_param_type

    def __str__(self) -> str:
        annotated_param_type_str = _param_type_to_user_string(self.annotated_param_type)
        default_param_type_str = _param_type_to_user_string(self.default_param_type)
        msg = f"Cannot specify {annotated_param_type_str} in `Annotated` and"
        if self.annotated_param_type is self.default_param_type:
            msg += " default value"
        else:
            msg += f" {default_param_type_str} as a default value"
        msg += f" together for {self.argument_name!r}"
        return msg


class MultipleTyperAnnotationsError(Exception):
    argument_name: str

    def __init__(self, argument_name: str):
        self.argument_name = argument_name

    def __str__(self) -> str:
        return (
            "Cannot specify multiple `Annotated` Typer arguments"
            f" for {self.argument_name!r}"
        )


class DefaultFactoryAndDefaultValueError(Exception):
    argument_name: str
    param_type: Type[ParameterInfo]

    def __init__(self, argument_name: str, param_type: Type[ParameterInfo]):
        self.argument_name = argument_name
        self.param_type = param_type

    def __str__(self) -> str:
        param_type_str = _param_type_to_user_string(self.param_type)
        return (
            "Cannot specify `default_factory` and a default value together"
            f" for {param_type_str}"
        )


def _split_annotation_from_typer_annotations(
    base_annotation: Type[Any],
) -> Tuple[Type[Any], List[ParameterInfo]]:
    if get_origin(base_annotation) is not Annotated:  # type: ignore
        return base_annotation, []
    base_annotation, *maybe_typer_annotations = get_args(base_annotation)
    return base_annotation, [
        annotation
        for annotation in maybe_typer_annotations
        if isinstance(annotation, ParameterInfo)
    ]


def _lenient_issubclass(
    cls: Any, class_or_tuple  # : Union[AnyType, Tuple[AnyType, ...]]
) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def _process_pydantic_model(model: "pydantic.BaseModel", names: List[str]):
    for field in model.__fields__.values():
        if _lenient_issubclass(field.type_, pydantic.BaseModel):
            names.append(field.name)
            yield from _process_pydantic_model(field.type_, names)
            names.pop()
        else:
            name = PYDANTIC_FIELD_DELIMITER.join(names + [field.name])
            yield name, ParamMeta(
                name=name, default=field.default, annotation=field.type_
            )


def _process_param_from_function(
    type_hints: Dict[str, Any], param: Parameter, expand_pydantic_fields: bool = True
) -> Tuple[str, ParamMeta]:
    annotation, typer_annotations = _split_annotation_from_typer_annotations(
        param.annotation,
    )
    if len(typer_annotations) > 1:
        raise MultipleTyperAnnotationsError(param.name)

    if (
        expand_pydantic_fields
        and pydantic
        and _lenient_issubclass(annotation, pydantic.BaseModel)
    ):
        yield from _process_pydantic_model(annotation, [param.name])
        return

    default = param.default
    if typer_annotations:
        # It's something like `my_param: Annotated[str, Argument()]`
        [parameter_info] = typer_annotations

        # Forbid `my_param: Annotated[str, Argument()] = Argument("...")`
        if isinstance(param.default, ParameterInfo):
            raise MixedAnnotatedAndDefaultStyleError(
                argument_name=param.name,
                annotated_param_type=type(parameter_info),
                default_param_type=type(param.default),
            )

        parameter_info = copy(parameter_info)

        # When used as a default, `Option` takes a default value and option names
        # as positional arguments:
        #   `Option(some_value, "--some-argument", "-s")`
        # When used in `Annotated` (ie, what this is handling), `Option` just takes
        # option names as positional arguments:
        #   `Option("--some-argument", "-s")`
        # In this case, the `default` attribute of `parameter_info` is actually
        # meant to be the first item of `param_decls`.
        if isinstance(parameter_info, OptionInfo) and parameter_info.default is not ...:
            parameter_info.param_decls = (
                cast(str, parameter_info.default),
                *(parameter_info.param_decls or ()),
            )
            parameter_info.default = ...

        # Forbid `my_param: Annotated[str, Argument('some-default')]`
        if parameter_info.default is not ...:
            raise AnnotatedParamWithDefaultValueError(
                param_type=type(parameter_info),
                argument_name=param.name,
            )
        if param.default is not param.empty:
            # Put the parameter's default (set by `=`) into `parameter_info`, where
            # typer can find it.
            parameter_info.default = param.default

        default = parameter_info
    elif param.name in type_hints:
        # Resolve forward references.
        annotation = type_hints[param.name]

    if isinstance(default, ParameterInfo):
        parameter_info = copy(default)
        # Click supports `default` as either
        # - an actual value; or
        # - a factory function (returning a default value.)
        # The two are not interchangeable for static typing, so typer allows
        # specifying `default_factory`. Move the `default_factory` into `default`
        # so click can find it.
        if parameter_info.default is ... and parameter_info.default_factory:
            parameter_info.default = parameter_info.default_factory
        elif parameter_info.default_factory:
            raise DefaultFactoryAndDefaultValueError(
                argument_name=param.name, param_type=type(parameter_info)
            )
        default = parameter_info
    yield param.name, ParamMeta(name=param.name, default=default, annotation=annotation)


def get_params_from_function(
    func: Callable[..., Any], expand_pydantic_fields: bool = True
) -> Dict[str, ParamMeta]:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        for name, meta in _process_param_from_function(
            type_hints, param, expand_pydantic_fields=expand_pydantic_fields
        ):
            params[name] = meta
    return params


def _explode_env_vars(
    env_nested_delimiter: str, env_vars: Dict[str, Optional[str]]
) -> Dict[str, Any]:
    """
    Process env_vars and extract the values of keys containing env_nested_delimiter into nested dictionaries.

    This is applied to a single field, hence filtering by env_var prefix.
    """
    prefixes = (
        []
    )  # f'{env_name}{env_nested_delimiter}' for env_name in field.field_info.extra['env_names']]
    result: Dict[str, Any] = {}
    for env_name, env_val in env_vars.items():
        # if not any(env_name.startswith(prefix) for prefix in prefixes):
        # continue
        # we remove the prefix before splitting in case the prefix has characters in common with the delimiter
        env_name_without_prefix = env_name  # [self.env_prefix_len :]
        _, *keys, last_key = env_name_without_prefix.split(env_nested_delimiter)
        env_var = result
        for key in keys:
            env_var = env_var.setdefault(key, {})
        env_var[last_key] = env_val

    return result


def update_pydantic_params(
    callback: Optional[Callable[..., Any]], use_params: Dict[str, Any]
) -> None:
    """
    Explode and collapse delimited params into pydantic models.

    Example:
      --foo--bar 23, --foo--baz 42
      -> {"foo": {"bar": 23, "baz" 42 }}
      -> {"foo": Foo(**{"bar": 23, "baz" 42 })}
    """
    if not pydantic:
        return use_params

    pydantic_parameters = {
        param_name: param.annotation
        for param_name, param in get_params_from_function(
            callback, expand_pydantic_fields=False
        ).items()
        if _lenient_issubclass(param.annotation, pydantic.BaseModel)
    }

    delimited_vars = {}
    delete = []
    for k, v in use_params.items():
        if PYDANTIC_FIELD_DELIMITER in k:
            if v is not None:
                delimited_vars[PYDANTIC_FIELD_DELIMITER + k] = v
            delete.append(k)
    for delete_one in delete:
        use_params.pop(delete_one)
    exploded_vars = _explode_env_vars(
        env_nested_delimiter=PYDANTIC_FIELD_DELIMITER, env_vars=delimited_vars
    )
    for k, v in exploded_vars.items():
        use_params[k] = pydantic_parameters[k](**v)
