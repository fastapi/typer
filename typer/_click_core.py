# Code adapted from Click 8.3.1

import os
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Mapping, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
    overload,
)

from . import BadParameter, MissingParameter
from ._click._utils import UNSET
from ._click.core import ParameterSource
from ._click.parser import _OptionParser
from ._click.types import (
    ParamType,
    convert_type,
)
from ._typing import Literal
from .context import Context, augment_usage_errors

if TYPE_CHECKING:
    from ._click.shell_completion import CompletionItem


def _check_iter(value: Any) -> Iterator[Any]:
    """Check if the value is iterable but not a string. Raises a type
    error, or return an iterator over the value.
    """
    if isinstance(value, str):
        raise TypeError

    return iter(value)


class Parameter(ABC):
    """A parameter is either an option or an argument.
    Some functionality is specific to either of the two,
    so this abstract class bundles what is supported for both.
    """

    param_type_name = "parameter"

    def __init__(
        self,
        param_decls: Sequence[str] | None = None,
        type: ParamType | Any | None = None,
        required: bool = False,
        default: Any | Callable[[], Any] | None = UNSET,
        callback: Callable[[Context, "Parameter", Any], Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | Sequence[str] | None = None,
        shell_complete: Callable[
            [Context, "Parameter", str], list[CompletionItem] | list[str]
        ]
        | None = None,
    ) -> None:
        self.name: str | None
        self.opts: list[str]
        self.secondary_opts: list[str]
        self.name, self.opts, self.secondary_opts = self._parse_decls(
            param_decls or (), expose_value
        )
        self.type: ParamType = convert_type(type, default)

        # Default nargs to what the type tells us if we have that
        # information available.
        if nargs is None:
            if self.type.is_composite:
                nargs = self.type.arity
            else:
                nargs = 1

        self.required = required
        self.callback = callback
        self.nargs = nargs
        self.multiple = multiple
        self.expose_value = expose_value
        self.default: Any | Callable[[], Any] | None = default
        self.is_eager = is_eager
        self.metavar = metavar
        self.envvar = envvar
        self._custom_shell_complete = shell_complete

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    @abstractmethod
    def _parse_decls(
        self, decls: Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]: ...

    @property
    def human_readable_name(self) -> str:
        """Returns the human readable name of this parameter.  This is the
        same as the name for options, but the metavar for arguments.
        """
        return self.name  # type: ignore

    def make_metavar(self, ctx: Context) -> str:
        if self.metavar is not None:
            return self.metavar

        metavar = self.type.get_metavar(param=self, ctx=ctx)

        if metavar is None:
            metavar = self.type.name.upper()

        if self.nargs != 1:
            metavar += "..."

        return metavar

    @overload
    def get_default(self, ctx: Context, call: Literal[True] = True) -> Any | None: ...

    @overload
    def get_default(
        self, ctx: Context, call: bool = ...
    ) -> Any | Callable[[], Any] | None: ...

    def get_default(
        self, ctx: Context, call: bool = True
    ) -> Any | Callable[[], Any] | None:
        """Get the default for the parameter."""
        value = ctx.lookup_default(self.name, call=False)  # type: ignore

        if value is UNSET:
            value = self.default

        if call and callable(value):
            value = value()

        return value

    @abstractmethod
    def add_to_parser(self, parser: _OptionParser, ctx: Context) -> None: ...

    def consume_value(
        self, ctx: Context, opts: Mapping[str, Any]
    ) -> tuple[Any, ParameterSource]:
        """Returns the parameter value produced by the parser."""
        # Collect from the parse the value passed by the user to the CLI.
        value = opts.get(self.name, UNSET)  # type: ignore
        # If the value is set, it means it was sourced from the command line by the
        # parser, otherwise it left unset by default.
        source = (
            ParameterSource.COMMANDLINE
            if value is not UNSET
            else ParameterSource.DEFAULT
        )

        if value is UNSET:
            envvar_value = self.value_from_envvar(ctx)
            if envvar_value is not None:
                value = envvar_value
                source = ParameterSource.ENVIRONMENT

        if value is UNSET:
            default_map_value = ctx.lookup_default(self.name)  # type: ignore
            if default_map_value is not UNSET:
                value = default_map_value
                source = ParameterSource.DEFAULT_MAP

        if value is UNSET:
            default_value = self.get_default(ctx)
            if default_value is not UNSET:
                value = default_value
                source = ParameterSource.DEFAULT

        return value, source

    def type_cast_value(self, ctx: Context, value: Any) -> Any:
        """Convert and validate a value against the parameter's
        :attr:`type`, :attr:`multiple`, and :attr:`nargs`.
        """
        if value is None:
            if self.multiple or self.nargs == -1:
                return ()
            else:
                return value

        def check_iter(value: Any) -> Iterator[Any]:
            try:
                return _check_iter(value)
            except TypeError:
                # This should only happen when passing in args manually,
                # the parser should construct an iterable when parsing
                # the command line.
                raise BadParameter(
                    "Value must be an iterable.", ctx=ctx, param=self
                ) from None

        # Define the conversion function based on nargs and type.

        if self.nargs == 1 or self.type.is_composite:

            def convert(value: Any) -> Any:
                return self.type(value, param=self, ctx=ctx)

        elif self.nargs == -1:

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                return tuple(self.type(x, self, ctx) for x in check_iter(value))

        # TODO: remove or test
        else:  # nargs > 1

            def convert(value: Any) -> Any:  # tuple[t.Any, ...]
                value = tuple(check_iter(value))

                if len(value) != self.nargs:
                    raise BadParameter(
                        f"Takes {self.nargs} values but {len(value)} were given.",
                        ctx=ctx,
                        param=self,
                    )

                return tuple(self.type(x, self, ctx) for x in value)

        if self.multiple:
            return tuple(convert(x) for x in check_iter(value))

        return convert(value)

    @abstractmethod
    def value_is_missing(self, value: Any) -> bool: ...

    def process_value(self, ctx: Context, value: Any) -> Any:
        """Process the value of this parameter:

        1. Type cast the value
        2. Check if the value is missing
        3. If a `callback` is set, call it to have the value replaced by the
           result of the callback. If the value was not set, the callback receive
           ``None``. This keep the legacy behavior as it was before the introduction of
           the :attr:`UNSET` sentinel.
        """
        # shelter `type_cast_value` from ever seeing an `UNSET` value by handling the
        # cases in which `UNSET` gets special treatment explicitly at this layer
        #
        # Refs:
        # https://github.com/pallets/click/issues/3069
        if value is UNSET:
            if self.multiple or self.nargs == -1:
                value = ()
        else:
            value = self.type_cast_value(ctx, value)

        if self.required and self.value_is_missing(value):
            raise MissingParameter(ctx=ctx, param=self)

        if self.callback is not None:
            # Legacy case: UNSET is not exposed directly to the callback, but converted
            # to None.
            if value is UNSET:
                value = None

            # Search for parameters with UNSET values in the context.
            unset_keys = {k: None for k, v in ctx.params.items() if v is UNSET}
            # No UNSET values, call the callback as usual.
            if not unset_keys:
                value = self.callback(ctx, self, value)

            # Legacy case: provide a temporarily manipulated context to the callback
            # to hide UNSET values as None.
            #
            # Refs:
            # https://github.com/pallets/click/issues/3136
            # https://github.com/pallets/click/pull/3137
            else:
                # Add another layer to the context stack to clearly hint that the
                # context is temporarily modified.
                with ctx:
                    # Update the context parameters to replace UNSET with None.
                    ctx.params.update(unset_keys)
                    # Feed these fake context parameters to the callback.
                    value = self.callback(ctx, self, value)
                    # Restore the UNSET values in the context parameters.
                    ctx.params.update(
                        {
                            k: UNSET
                            for k in unset_keys
                            # Only restore keys that are present and still None, in case
                            # the callback modified other parameters.
                            if k in ctx.params and ctx.params[k] is None
                        }
                    )

        return value

    def resolve_envvar_value(self, ctx: Context) -> str | None:
        """Returns the value found in the environment variable(s) attached to this
        parameter.

        Environment variables values are `always returned as strings
        <https://docs.python.org/3/library/os.html#os.environ>`_.

        This method returns ``None`` if:

        - the :attr:`envvar` property is not set on the :class:`Parameter`,
        - the environment variable is not found in the environment,
        - the variable is found in the environment but its value is empty (i.e. the
          environment variable is present but has an empty string).

        If :attr:`envvar` is setup with multiple environment variables,
        then only the first non-empty value is returned.

        .. caution::

            The raw value extracted from the environment is not normalized and is
            returned as-is. Any normalization or reconciliation is performed later by
            the :class:`Parameter`'s :attr:`type`.
        """
        if not self.envvar:
            return None

        if isinstance(self.envvar, str):
            rv = os.environ.get(self.envvar)

            if rv:
                return rv
        else:
            for envvar in self.envvar:
                rv = os.environ.get(envvar)

                # Return the first non-empty value of the list of environment variables.
                if rv:
                    return rv
                # Else, absence of value is interpreted as an environment variable that
                # is not set, so proceed to the next one.

        return None

    def value_from_envvar(self, ctx: Context) -> str | Sequence[str] | None:
        """Process the raw environment variable string for this parameter.

        Returns the string as-is or splits it into a sequence of strings if the
        parameter is expecting multiple values (i.e. its :attr:`nargs` property is set
        to a value other than ``1``).
        """
        rv = self.resolve_envvar_value(ctx)

        if rv is not None and self.nargs != 1:
            return self.type.split_envvar_value(rv)

        return rv

    def handle_parse_result(
        self, ctx: Context, opts: Mapping[str, Any], args: list[str]
    ) -> tuple[Any, list[str]]:
        """Process the value produced by the parser from user input.

        Always process the value through the Parameter's :attr:`type`, wherever it
        comes from.
        """
        with augment_usage_errors(ctx, param=self):
            value, source = self.consume_value(ctx, opts)

            ctx.set_parameter_source(self.name, source)  # type: ignore

            # Process the value through the parameter's type.
            try:
                value = self.process_value(ctx, value)
            except Exception:
                if not ctx.resilient_parsing:
                    raise
                # In resilient parsing mode, we do not want to fail the command if the
                # value is incompatible with the parameter type, so we reset the value
                # to UNSET, which will be interpreted as a missing value.
                value = UNSET

        # Add parameter's value to the context.
        if (
            self.expose_value
            # We skip adding the value if it was previously set by another parameter
            # targeting the same variable name. This prevents parameters competing for
            # the same name to override each other.
            and (self.name not in ctx.params or ctx.params[self.name] is UNSET)
        ):
            # Click is logically enforcing that the name is None if the parameter is
            # not to be exposed. We still assert it here to please the type checker.
            assert self.name is not None, (
                f"{self!r} parameter's name should not be None when exposing value."
            )
            ctx.params[self.name] = value

        return value, args

    @abstractmethod
    def get_help_record(self, ctx: Context) -> tuple[str, str] | None: ...

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return []

    def get_error_hint(self, ctx: Context) -> str:
        """Get a stringified version of the param for use in error messages to
        indicate which param caused the error.
        """
        hint_list = self.opts or [self.human_readable_name]
        return " / ".join(f"'{x}'" for x in hint_list)

    def shell_complete(self, ctx: Context, incomplete: str) -> list[CompletionItem]:
        """Return a list of completions for the incomplete value."""
        if self._custom_shell_complete is not None:
            results = self._custom_shell_complete(ctx, self, incomplete)

            if results and isinstance(results[0], str):
                results = [CompletionItem(c) for c in results]

            return cast("list[CompletionItem]", results)

        return self.type.shell_complete(ctx, self, incomplete)
