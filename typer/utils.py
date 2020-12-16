import inspect
import logging

from typing import Any, Callable, Dict, get_type_hints

from .models import ParamMeta


class TyperLoggerHandler(logging.Handler):
    """ A custom logger handler that use Typer echo. """

    def emit(self, record: logging.LogRecord) -> None:
        echo(self.format(record))

        
def get_params_from_function(func: Callable[..., Any]) -> Dict[str, ParamMeta]:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]
        params[param.name] = ParamMeta(
            name=param.name, default=param.default, annotation=annotation
        )
    return params
