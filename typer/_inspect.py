import inspect
import sys

if sys.version_info >= (3, 10):
    from inspect import signature
elif sys.version_info >= (3, 8):
    from typing import Any, Callable

    from typing_extensions import get_annotations

    def signature(
        func: Callable[..., Any], eval_str: bool = False, **kwargs: Any
    ) -> inspect.Signature:
        sig = inspect.signature(func, **kwargs)
        ann = get_annotations(
            func,
            globals=kwargs.get("globals"),
            locals=kwargs.get("locals"),
            eval_str=eval_str,
        )
        return sig.replace(
            parameters=[
                param.replace(annotation=ann.get(name, param.annotation))
                for name, param in sig.parameters.items()
            ],
            return_annotation=ann.get("return", sig.return_annotation),
        )
else:
    # Fallback for Python <3.8 to make `inspect.signature` accept the `eval_str`
    # keyword argument as a no-op. We can't backport support for evaluating
    # string annotations because only typing-extensions v4.13.0+ provides a
    # backport of `inspect.get_annotations`, which requires Python 3.8+.

    from typing import Any, Callable

    def signature(
        func: Callable[..., Any], eval_str: bool = False, **kwargs: Any
    ) -> inspect.Signature:
        return inspect.signature(func, **kwargs)


__all__ = ["signature"]
