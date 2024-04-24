import inspect
from typing import Annotated, Any, Callable

import pydantic
from pydantic._internal._utils import deep_update
from pydantic_core import PydanticUndefined

from .params import Option
from .utils import inspect_signature

PYDANTIC_FIELD_SEPARATOR = "."


def flatten_pydantic_model(
    model: pydantic.BaseModel, ancestors: list[str]
) -> dict[str, inspect.Parameter]:
    from .main import lenient_issubclass

    pydantic_parameters = {}
    for field_name, field in model.model_fields.items():
        qualifier = [*ancestors, field_name]
        sub_name = f"_pydantic_{'_'.join(qualifier)}"
        if lenient_issubclass(field.annotation, pydantic.BaseModel):
            params = flatten_pydantic_model(field.annotation, qualifier)  # type: ignore[arg-type]
            pydantic_parameters.update(params)
        else:
            default = field.default if field.default != PydanticUndefined else ...
            typer_option = Option(f"--{PYDANTIC_FIELD_SEPARATOR.join(qualifier)}")
            pydantic_parameters[sub_name] = inspect.Parameter(
                sub_name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=Annotated[field.annotation, typer_option, qualifier],
                default=default,
            )
    return pydantic_parameters


def wrap_pydantic_callback(callback: Callable[..., Any]) -> Callable[..., Any]:
    from .main import lenient_issubclass

    original_signature = inspect_signature(callback)

    pydantic_parameters = {}
    pydantic_roots = {}
    other_parameters = {}
    for name, parameter in original_signature.parameters.items():
        if lenient_issubclass(parameter.annotation, pydantic.BaseModel):
            params = flatten_pydantic_model(parameter.annotation, [name])
            pydantic_parameters.update(params)
            pydantic_roots[name] = parameter.annotation
        else:
            other_parameters[name] = parameter

    extended_signature = inspect.Signature(
        [*other_parameters.values(), *pydantic_parameters.values()],
        return_annotation=original_signature.return_annotation,
    )

    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        converted_kwargs = kwargs.copy()
        pydantic_dicts: dict[str, Any] = {}
        for kwarg_name, kwarg_value in kwargs.items():
            if kwarg_name in pydantic_parameters:
                converted_kwargs.pop(kwarg_name)
                annotation = pydantic_parameters[kwarg_name].annotation
                _, qualifier = annotation.__metadata__
                for part in reversed(qualifier):
                    kwarg_value = {part: kwarg_value}
                pydantic_dicts = deep_update(pydantic_dicts, kwarg_value)
        for root_name, value in pydantic_dicts.items():
            converted_kwargs[root_name] = pydantic_roots[root_name](**value)
        return callback(*args, **converted_kwargs)

    wrapper.__signature__ = extended_signature  # type: ignore
    return wrapper
