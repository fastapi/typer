from __future__ import annotations

import collections.abc as cabc
import enum
import inspect
import os
import typing as t
from gettext import gettext as _
from gettext import ngettext
from itertools import repeat

from .. import Context
from ..context import augment_usage_errors
from . import types
from ._utils import FLAG_NEEDS_VALUE, UNSET
from .exceptions import (
    BadParameter,
    MissingParameter,
)
from .formatting import join_options
from .parser import _OptionParser, _split_opt
from .termui import confirm, prompt, style
from .utils import echo

if t.TYPE_CHECKING:
    from .shell_completion import CompletionItem


V = t.TypeVar("V")


def batch(iterable: cabc.Iterable[V], batch_size: int) -> list[tuple[V, ...]]:
    return list(zip(*repeat(iter(iterable), batch_size), strict=False))


class ParameterSource(enum.Enum):
    """This is an :class:`~enum.Enum` that indicates the source of a
    parameter's value.

    Use :meth:`click.Context.get_parameter_source` to get the
    source for a parameter by name.

    .. versionchanged:: 8.0
        Use :class:`~enum.Enum` and drop the ``validate`` method.

    .. versionchanged:: 8.0
        Added the ``PROMPT`` value.
    """

    COMMANDLINE = enum.auto()
    """The value was provided by the command line args."""
    ENVIRONMENT = enum.auto()
    """The value was provided with an environment variable."""
    DEFAULT = enum.auto()
    """Used the default specified by the parameter."""
    DEFAULT_MAP = enum.auto()
    """Used a default provided by :attr:`Context.default_map`."""
    PROMPT = enum.auto()
    """Used a prompt to confirm a default or provide a value."""


def _check_iter(value: t.Any) -> cabc.Iterator[t.Any]:
    """Check if the value is iterable but not a string. Raises a type
    error, or return an iterator over the value.
    """
    if isinstance(value, str):
        raise TypeError

    return iter(value)


class Parameter:
    r"""A parameter to a command comes in two versions: they are either
    :class:`Option`\s or :class:`Argument`\s.  Other subclasses are currently
    not supported by design as some of the internals for parsing are
    intentionally not finalized.

    Some settings are supported by both options and arguments.

    :param param_decls: the parameter declarations for this option or
                        argument.  This is a list of flags or argument
                        names.
    :param type: the type that should be used.  Either a :class:`ParamType`
                 or a Python type.  The latter is converted into the former
                 automatically if supported.
    :param required: controls if this is optional or not.
    :param default: the default value if omitted.  This can also be a callable,
                    in which case it's invoked when the default is needed
                    without any arguments.
    :param callback: A function to further process or validate the value
        after type conversion. It is called as ``f(ctx, param, value)``
        and must return the value. It is called for all sources,
        including prompts.
    :param nargs: the number of arguments to match.  If not ``1`` the return
                  value is a tuple instead of single value.  The default for
                  nargs is ``1`` (except if the type is a tuple, then it's
                  the arity of the tuple). If ``nargs=-1``, all remaining
                  parameters are collected.
    :param metavar: how the value is represented in the help page.
    :param expose_value: if this is `True` then the value is passed onwards
                         to the command callback and stored on the context,
                         otherwise it's skipped.
    :param is_eager: eager values are processed before non eager ones.  This
                     should not be set for arguments or it will inverse the
                     order of processing.
    :param envvar: environment variable(s) that are used to provide a default value for
        this parameter. This can be a string or a sequence of strings. If a sequence is
        given, only the first non-empty environment variable is used for the parameter.
    :param shell_complete: A function that returns custom shell
        completions. Used instead of the param's type completion if
        given. Takes ``ctx, param, incomplete`` and must return a list
        of :class:`~click.shell_completion.CompletionItem` or a list of
        strings.
    :param deprecated: If ``True`` or non-empty string, issues a message
                        indicating that the argument is deprecated and highlights
                        its deprecation in --help. The message can be customized
                        by using a string as the value. A deprecated parameter
                        cannot be required, a ValueError will be raised otherwise.
    """

    param_type_name = "parameter"

    def __init__(
        self,
        param_decls: cabc.Sequence[str] | None = None,
        type: types.ParamType | t.Any | None = None,
        required: bool = False,
        # XXX The default historically embed two concepts:
        # - the declaration of a Parameter object carrying the default (handy to
        #   arbitrage the default value of coupled Parameters sharing the same
        #   self.name, like flag options),
        # - and the actual value of the default.
        # It is confusing and is the source of many issues discussed in:
        # https://github.com/pallets/click/pull/3030
        # In the future, we might think of splitting it in two, not unlike
        # Option.is_flag and Option.flag_value: we could have something like
        # Parameter.is_default and Parameter.default_value.
        default: t.Any | t.Callable[[], t.Any] | None = UNSET,
        callback: t.Callable[[Context, Parameter, t.Any], t.Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | cabc.Sequence[str] | None = None,
        shell_complete: t.Callable[
            [Context, Parameter, str], list[CompletionItem] | list[str]
        ]
        | None = None,
        deprecated: bool | str = False,
    ) -> None:
        self.name: str | None
        self.opts: list[str]
        self.secondary_opts: list[str]
        self.name, self.opts, self.secondary_opts = self._parse_decls(
            param_decls or (), expose_value
        )
        self.type: types.ParamType = types.convert_type(type, default)

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
        self.default: t.Any | t.Callable[[], t.Any] | None = default
        self.is_eager = is_eager
        self.metavar = metavar
        self.envvar = envvar
        self._custom_shell_complete = shell_complete
        self.deprecated = deprecated

        if __debug__:
            if self.type.is_composite and nargs != self.type.arity:
                raise ValueError(
                    f"'nargs' must be {self.type.arity} (or None) for"
                    f" type {self.type!r}, but it was {nargs}."
                )

            if required and deprecated:
                raise ValueError(
                    f"The {self.param_type_name} '{self.human_readable_name}' "
                    "is deprecated and still required. A deprecated "
                    f"{self.param_type_name} cannot be required."
                )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def _parse_decls(
        self, decls: cabc.Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        raise NotImplementedError()

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

    @t.overload
    def get_default(
        self, ctx: Context, call: t.Literal[True] = True
    ) -> t.Any | None: ...

    @t.overload
    def get_default(
        self, ctx: Context, call: bool = ...
    ) -> t.Any | t.Callable[[], t.Any] | None: ...

    def get_default(
        self, ctx: Context, call: bool = True
    ) -> t.Any | t.Callable[[], t.Any] | None:
        """Get the default for the parameter. Tries
        :meth:`Context.lookup_default` first, then the local default.

        :param ctx: Current context.
        :param call: If the default is a callable, call it. Disable to
            return the callable instead.

        .. versionchanged:: 8.0.2
            Type casting is no longer performed when getting a default.

        .. versionchanged:: 8.0.1
            Type casting can fail in resilient parsing mode. Invalid
            defaults will not prevent showing help text.

        .. versionchanged:: 8.0
            Looks at ``ctx.default_map`` first.

        .. versionchanged:: 8.0
            Added the ``call`` parameter.
        """
        value = ctx.lookup_default(self.name, call=False)  # type: ignore

        if value is UNSET:
            value = self.default

        if call and callable(value):
            value = value()

        return value

    def add_to_parser(self, parser: _OptionParser, ctx: Context) -> None:
        raise NotImplementedError()

    def consume_value(
        self, ctx: Context, opts: cabc.Mapping[str, t.Any]
    ) -> tuple[t.Any, ParameterSource]:
        """Returns the parameter value produced by the parser.

        If the parser did not produce a value from user input, the value is either
        sourced from the environment variable, the default map, or the parameter's
        default value. In that order of precedence.

        If no value is found, an internal sentinel value is returned.

        :meta private:
        """
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

    def type_cast_value(self, ctx: Context, value: t.Any) -> t.Any:
        """Convert and validate a value against the parameter's
        :attr:`type`, :attr:`multiple`, and :attr:`nargs`.
        """
        if value is None:
            if self.multiple or self.nargs == -1:
                return ()
            else:
                return value

        def check_iter(value: t.Any) -> cabc.Iterator[t.Any]:
            try:
                return _check_iter(value)
            except TypeError:
                # This should only happen when passing in args manually,
                # the parser should construct an iterable when parsing
                # the command line.
                raise BadParameter(
                    _("Value must be an iterable."), ctx=ctx, param=self
                ) from None

        # Define the conversion function based on nargs and type.

        if self.nargs == 1 or self.type.is_composite:

            def convert(value: t.Any) -> t.Any:
                return self.type(value, param=self, ctx=ctx)

        elif self.nargs == -1:

            def convert(value: t.Any) -> t.Any:  # tuple[t.Any, ...]
                return tuple(self.type(x, self, ctx) for x in check_iter(value))

        else:  # nargs > 1

            def convert(value: t.Any) -> t.Any:  # tuple[t.Any, ...]
                value = tuple(check_iter(value))

                if len(value) != self.nargs:
                    raise BadParameter(
                        ngettext(
                            "Takes {nargs} values but 1 was given.",
                            "Takes {nargs} values but {len} were given.",
                            len(value),
                        ).format(nargs=self.nargs, len=len(value)),
                        ctx=ctx,
                        param=self,
                    )

                return tuple(self.type(x, self, ctx) for x in value)

        if self.multiple:
            return tuple(convert(x) for x in check_iter(value))

        return convert(value)

    def value_is_missing(self, value: t.Any) -> bool:
        """A value is considered missing if:

        - it is :attr:`UNSET`,
        - or if it is an empty sequence while the parameter is suppose to have
          non-single value (i.e. :attr:`nargs` is not ``1`` or :attr:`multiple` is
          set).

        :meta private:
        """
        if value is UNSET:
            return True

        if (self.nargs != 1 or self.multiple) and value == ():
            return True

        return False

    def process_value(self, ctx: Context, value: t.Any) -> t.Any:
        """Process the value of this parameter:

        1. Type cast the value using :meth:`type_cast_value`.
        2. Check if the value is missing (see: :meth:`value_is_missing`), and raise
           :exc:`MissingParameter` if it is required.
        3. If a :attr:`callback` is set, call it to have the value replaced by the
           result of the callback. If the value was not set, the callback receive
           ``None``. This keep the legacy behavior as it was before the introduction of
           the :attr:`UNSET` sentinel.

        :meta private:
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

        :meta private:
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

    def value_from_envvar(self, ctx: Context) -> str | cabc.Sequence[str] | None:
        """Process the raw environment variable string for this parameter.

        Returns the string as-is or splits it into a sequence of strings if the
        parameter is expecting multiple values (i.e. its :attr:`nargs` property is set
        to a value other than ``1``).

        :meta private:
        """
        rv = self.resolve_envvar_value(ctx)

        if rv is not None and self.nargs != 1:
            return self.type.split_envvar_value(rv)

        return rv

    def handle_parse_result(
        self, ctx: Context, opts: cabc.Mapping[str, t.Any], args: list[str]
    ) -> tuple[t.Any, list[str]]:
        """Process the value produced by the parser from user input.

        Always process the value through the Parameter's :attr:`type`, wherever it
        comes from.

        If the parameter is deprecated, this method warn the user about it. But only if
        the value has been explicitly set by the user (and as such, is not coming from
        a default).

        :meta private:
        """
        with augment_usage_errors(ctx, param=self):
            value, source = self.consume_value(ctx, opts)

            ctx.set_parameter_source(self.name, source)  # type: ignore

            # Display a deprecation warning if necessary.
            if (
                self.deprecated
                and value is not UNSET
                and source not in (ParameterSource.DEFAULT, ParameterSource.DEFAULT_MAP)
            ):
                extra_message = (
                    f" {self.deprecated}" if isinstance(self.deprecated, str) else ""
                )
                message = _(
                    "DeprecationWarning: The {param_type} {name!r} is deprecated."
                    "{extra_message}"
                ).format(
                    param_type=self.param_type_name,
                    name=self.human_readable_name,
                    extra_message=extra_message,
                )
                echo(style(message, fg="red"), err=True)

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

    def get_help_record(self, ctx: Context) -> tuple[str, str] | None:
        pass

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return []

    def get_error_hint(self, ctx: Context) -> str:
        """Get a stringified version of the param for use in error messages to
        indicate which param caused the error.
        """
        hint_list = self.opts or [self.human_readable_name]
        return " / ".join(f"'{x}'" for x in hint_list)

    def shell_complete(self, ctx: Context, incomplete: str) -> list[CompletionItem]:
        """Return a list of completions for the incomplete value. If a
        ``shell_complete`` function was given during init, it is used.
        Otherwise, the :attr:`type`
        :meth:`~click.types.ParamType.shell_complete` function is used.

        :param ctx: Invocation context for this command.
        :param incomplete: Value being completed. May be empty.

        .. versionadded:: 8.0
        """
        if self._custom_shell_complete is not None:
            results = self._custom_shell_complete(ctx, self, incomplete)

            if results and isinstance(results[0], str):
                from .shell_completion import CompletionItem

                results = [CompletionItem(c) for c in results]

            return t.cast("list[CompletionItem]", results)

        return self.type.shell_complete(ctx, self, incomplete)


class Option(Parameter):
    """Options are usually optional values on the command line and
    have some extra features that arguments don't have.

    All other parameters are passed onwards to the parameter constructor.

    :param show_default: Show the default value for this option in its
        help text. Values are not shown by default, unless
        :attr:`Context.show_default` is ``True``. If this value is a
        string, it shows that string in parentheses instead of the
        actual value. This is particularly useful for dynamic options.
        For single option boolean flags, the default remains hidden if
        its value is ``False``.
    :param show_envvar: Controls if an environment variable should be
        shown on the help page and error messages.
        Normally, environment variables are not shown.
    :param prompt: If set to ``True`` or a non empty string then the
        user will be prompted for input. If set to ``True`` the prompt
        will be the option name capitalized. A deprecated option cannot be
        prompted.
    :param confirmation_prompt: Prompt a second time to confirm the
        value if it was prompted for. Can be set to a string instead of
        ``True`` to customize the message.
    :param prompt_required: If set to ``False``, the user will be
        prompted for input only when the option was specified as a flag
        without a value.
    :param hide_input: If this is ``True`` then the input on the prompt
        will be hidden from the user. This is useful for password input.
    :param is_flag: forces this option to act as a flag.  The default is
                    auto detection.
    :param flag_value: which value should be used for this flag if it's
                       enabled.  This is set to a boolean automatically if
                       the option string contains a slash to mark two options.
    :param multiple: if this is set to `True` then the argument is accepted
                     multiple times and recorded.  This is similar to ``nargs``
                     in how it works but supports arbitrary number of
                     arguments.
    :param count: this flag makes an option increment an integer.
    :param allow_from_autoenv: if this is enabled then the value of this
                               parameter will be pulled from an environment
                               variable in case a prefix is defined on the
                               context.
    :param help: the help string.
    :param hidden: hide this option from help outputs.
    :param attrs: Other command arguments described in :class:`Parameter`.

    .. versionchanged:: 8.2
        ``envvar`` used with ``flag_value`` will always use the ``flag_value``,
        previously it would use the value of the environment variable.

    .. versionchanged:: 8.1
        Help text indentation is cleaned here instead of only in the
        ``@option`` decorator.

    .. versionchanged:: 8.1
        The ``show_default`` parameter overrides
        ``Context.show_default``.

    .. versionchanged:: 8.1
        The default of a single option boolean flag is not shown if the
        default value is ``False``.

    .. versionchanged:: 8.0.1
        ``type`` is detected from ``flag_value`` if given.
    """

    param_type_name = "option"

    def __init__(
        self,
        param_decls: cabc.Sequence[str] | None = None,
        show_default: bool | str | None = None,
        prompt: bool | str = False,
        confirmation_prompt: bool | str = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: bool | None = None,
        flag_value: t.Any = UNSET,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        type: types.ParamType | t.Any | None = None,
        help: str | None = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        deprecated: bool | str = False,
        **attrs: t.Any,
    ) -> None:
        if help:
            help = inspect.cleandoc(help)

        super().__init__(
            param_decls, type=type, multiple=multiple, deprecated=deprecated, **attrs
        )

        if prompt is True:
            if self.name is None:
                raise TypeError("'name' is required with 'prompt=True'.")

            prompt_text: str | None = self.name.replace("_", " ").capitalize()
        elif prompt is False:
            prompt_text = None
        else:
            prompt_text = prompt

        if deprecated:
            deprecated_message = (
                f"(DEPRECATED: {deprecated})"
                if isinstance(deprecated, str)
                else "(DEPRECATED)"
            )
            help = help + deprecated_message if help is not None else deprecated_message

        self.prompt = prompt_text
        self.confirmation_prompt = confirmation_prompt
        self.prompt_required = prompt_required
        self.hide_input = hide_input
        self.hidden = hidden

        # The _flag_needs_value property tells the parser that this option is a flag
        # that cannot be used standalone and needs a value. With this information, the
        # parser can determine whether to consider the next user-provided argument in
        # the CLI as a value for this flag or as a new option.
        # If prompt is enabled but not required, then it opens the possibility for the
        # option to gets its value from the user.
        self._flag_needs_value = self.prompt is not None and not self.prompt_required

        # Auto-detect if this is a flag or not.
        if is_flag is None:
            # Implicitly a flag because flag_value was set.
            if flag_value is not UNSET:
                is_flag = True
            # Not a flag, but when used as a flag it shows a prompt.
            elif self._flag_needs_value:
                is_flag = False
            # Implicitly a flag because secondary options names were given.
            elif self.secondary_opts:
                is_flag = True
        # The option is explicitly not a flag. But we do not know yet if it needs a
        # value or not. So we look at the default value to determine it.
        elif is_flag is False and not self._flag_needs_value:
            self._flag_needs_value = self.default is UNSET

        if is_flag:
            # Set missing default for flags if not explicitly required or prompted.
            if self.default is UNSET and not self.required and not self.prompt:
                if multiple:
                    self.default = ()

            # Auto-detect the type of the flag based on the flag_value.
            if type is None:
                # A flag without a flag_value is a boolean flag.
                if flag_value is UNSET:
                    self.type: types.ParamType = types.BoolParamType()
                # If the flag value is a boolean, use BoolParamType.
                elif isinstance(flag_value, bool):
                    self.type = types.BoolParamType()
                # Otherwise, guess the type from the flag value.
                else:
                    self.type = types.convert_type(None, flag_value)

        self.is_flag: bool = bool(is_flag)
        self.is_bool_flag: bool = bool(
            is_flag and isinstance(self.type, types.BoolParamType)
        )
        self.flag_value: t.Any = flag_value

        # Set boolean flag default to False if unset and not required.
        if self.is_bool_flag:
            if self.default is UNSET and not self.required:
                self.default = False

        # Support the special case of aligning the default value with the flag_value
        # for flags whose default is explicitly set to True. Note that as long as we
        # have this condition, there is no way a flag can have a default set to True,
        # and a flag_value set to something else. Refs:
        # https://github.com/pallets/click/issues/3024#issuecomment-3146199461
        # https://github.com/pallets/click/pull/3030/commits/06847da
        if self.default is True and self.flag_value is not UNSET:
            self.default = self.flag_value

        # Set the default flag_value if it is not set.
        if self.flag_value is UNSET:
            if self.is_flag:
                self.flag_value = True
            else:
                self.flag_value = None

        # Counting.
        self.count = count
        if count:
            if type is None:
                self.type = types.IntRange(min=0)
            if self.default is UNSET:
                self.default = 0

        self.allow_from_autoenv = allow_from_autoenv
        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar

        if __debug__:
            if deprecated and prompt:
                raise ValueError("`deprecated` options cannot use `prompt`.")

            if self.nargs == -1:
                raise TypeError("nargs=-1 is not supported for options.")

            if not self.is_bool_flag and self.secondary_opts:
                raise TypeError("Secondary flag is not valid for non-boolean flag.")

            if self.is_bool_flag and self.hide_input and self.prompt is not None:
                raise TypeError(
                    "'prompt' with 'hide_input' is not valid for boolean flag."
                )

            if self.count:
                if self.multiple:
                    raise TypeError("'count' is not valid with 'multiple'.")

                if self.is_flag:
                    raise TypeError("'count' is not valid with 'is_flag'.")

    def get_error_hint(self, ctx: Context) -> str:
        result = super().get_error_hint(ctx)
        if self.show_envvar and self.envvar is not None:
            result += f" (env var: '{self.envvar}')"
        return result

    def _parse_decls(
        self, decls: cabc.Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        opts = []
        secondary_opts = []
        name = None
        possible_names = []

        for decl in decls:
            if decl.isidentifier():
                if name is not None:
                    raise TypeError(f"Name '{name}' defined twice")
                name = decl
            else:
                split_char = ";" if decl[:1] == "/" else "/"
                if split_char in decl:
                    first, second = decl.split(split_char, 1)
                    first = first.rstrip()
                    if first:
                        possible_names.append(_split_opt(first))
                        opts.append(first)
                    second = second.lstrip()
                    if second:
                        secondary_opts.append(second.lstrip())
                    if first == second:
                        raise ValueError(
                            f"Boolean option {decl!r} cannot use the"
                            " same flag for true/false."
                        )
                else:
                    possible_names.append(_split_opt(decl))
                    opts.append(decl)

        if name is None and possible_names:
            possible_names.sort(key=lambda x: -len(x[0]))  # group long options first
            name = possible_names[0][1].replace("-", "_").lower()
            if not name.isidentifier():
                name = None

        if name is None:
            if not expose_value:
                return None, opts, secondary_opts
            raise TypeError(
                f"Could not determine name for option with declarations {decls!r}"
            )

        if not opts and not secondary_opts:
            raise TypeError(
                f"No options defined but a name was passed ({name})."
                " Did you mean to declare an argument instead? Did"
                f" you mean to pass '--{name}'?"
            )

        return name, opts, secondary_opts

    def add_to_parser(self, parser: _OptionParser, ctx: Context) -> None:
        if self.multiple:
            action = "append"
        elif self.count:
            action = "count"
        else:
            action = "store"

        if self.is_flag:
            action = f"{action}_const"

            if self.is_bool_flag and self.secondary_opts:
                parser.add_option(
                    obj=self, opts=self.opts, dest=self.name, action=action, const=True
                )
                parser.add_option(
                    obj=self,
                    opts=self.secondary_opts,
                    dest=self.name,
                    action=action,
                    const=False,
                )
            else:
                parser.add_option(
                    obj=self,
                    opts=self.opts,
                    dest=self.name,
                    action=action,
                    const=self.flag_value,
                )
        else:
            parser.add_option(
                obj=self,
                opts=self.opts,
                dest=self.name,
                action=action,
                nargs=self.nargs,
            )

    def get_help_record(self, ctx: Context) -> tuple[str, str] | None:
        if self.hidden:
            return None

        any_prefix_is_slash = False

        def _write_opts(opts: cabc.Sequence[str]) -> str:
            nonlocal any_prefix_is_slash

            rv, any_slashes = join_options(opts)

            if any_slashes:
                any_prefix_is_slash = True

            if not self.is_flag and not self.count:
                rv += f" {self.make_metavar(ctx=ctx)}"

            return rv

        rv = [_write_opts(self.opts)]

        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ""

        extra = self.get_help_extra(ctx)
        extra_items = []
        if "envvars" in extra:
            extra_items.append(
                _("env var: {var}").format(var=", ".join(extra["envvars"]))
            )
        if "default" in extra:
            extra_items.append(_("default: {default}").format(default=extra["default"]))
        if "range" in extra:
            extra_items.append(extra["range"])
        if "required" in extra:
            extra_items.append(_(extra["required"]))

        if extra_items:
            extra_str = "; ".join(extra_items)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"

        return ("; " if any_prefix_is_slash else " / ").join(rv), help

    def get_help_extra(self, ctx: Context) -> types.OptionHelpExtra:
        extra: types.OptionHelpExtra = {}

        if self.show_envvar:
            envvar = self.envvar

            if envvar is None:
                if (
                    self.allow_from_autoenv
                    and ctx.auto_envvar_prefix is not None
                    and self.name is not None
                ):
                    envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"

            if envvar is not None:
                if isinstance(envvar, str):
                    extra["envvars"] = (envvar,)
                else:
                    extra["envvars"] = tuple(str(d) for d in envvar)

        # Temporarily enable resilient parsing to avoid type casting
        # failing for the default. Might be possible to extend this to
        # help formatting in general.
        resilient = ctx.resilient_parsing
        ctx.resilient_parsing = True

        try:
            default_value = self.get_default(ctx, call=False)
        finally:
            ctx.resilient_parsing = resilient

        show_default = False
        show_default_is_str = False

        if self.show_default is not None:
            if isinstance(self.show_default, str):
                show_default_is_str = show_default = True
            else:
                show_default = self.show_default
        elif ctx.show_default is not None:
            show_default = ctx.show_default

        if show_default_is_str or (
            show_default and (default_value not in (None, UNSET))
        ):
            if show_default_is_str:
                default_string = f"({self.show_default})"
            elif isinstance(default_value, (list, tuple)):
                default_string = ", ".join(str(d) for d in default_value)
            elif isinstance(default_value, enum.Enum):
                default_string = default_value.name
            elif inspect.isfunction(default_value):
                default_string = _("(dynamic)")
            elif self.is_bool_flag and self.secondary_opts:
                # For boolean flags that have distinct True/False opts,
                # use the opt without prefix instead of the value.
                default_string = _split_opt(
                    (self.opts if default_value else self.secondary_opts)[0]
                )[1]
            elif self.is_bool_flag and not self.secondary_opts and not default_value:
                default_string = ""
            elif default_value == "":
                default_string = '""'
            else:
                default_string = str(default_value)

            if default_string:
                extra["default"] = default_string

        if (
            isinstance(self.type, types._NumberRangeBase)
            # skip count with default range type
            and not (self.count and self.type.min == 0 and self.type.max is None)
        ):
            range_str = self.type._describe_range()

            if range_str:
                extra["range"] = range_str

        if self.required:
            extra["required"] = "required"

        return extra

    def prompt_for_value(self, ctx: Context) -> t.Any:
        """This is an alternative flow that can be activated in the full
        value processing if a value does not exist.  It will prompt the
        user until a valid value exists and then returns the processed
        value as result.
        """
        assert self.prompt is not None

        # Calculate the default before prompting anything to lock in the value before
        # attempting any user interaction.
        default = self.get_default(ctx)

        # A boolean flag can use a simplified [y/n] confirmation prompt.
        if self.is_bool_flag:
            # If we have no boolean default, we force the user to explicitly provide
            # one.
            if default in (UNSET, None):
                default = None
            # Nothing prevent you to declare an option that is simultaneously:
            # 1) auto-detected as a boolean flag,
            # 2) allowed to prompt, and
            # 3) still declare a non-boolean default.
            # This forced casting into a boolean is necessary to align any non-boolean
            # default to the prompt, which is going to be a [y/n]-style confirmation
            # because the option is still a boolean flag. That way, instead of [y/n],
            # we get [Y/n] or [y/N] depending on the truthy value of the default.
            # Refs: https://github.com/pallets/click/pull/3030#discussion_r2289180249
            else:
                default = bool(default)
            return confirm(self.prompt, default)

        # If show_default is set to True/False, provide this to `prompt` as well. For
        # non-bool values of `show_default`, we use `prompt`'s default behavior
        prompt_kwargs: t.Any = {}
        if isinstance(self.show_default, bool):
            prompt_kwargs["show_default"] = self.show_default

        return prompt(
            self.prompt,
            # Use ``None`` to inform the prompt() function to reiterate until a valid
            # value is provided by the user if we have no default.
            default=None if default is UNSET else default,
            type=self.type,
            hide_input=self.hide_input,
            show_choices=self.show_choices,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_value(ctx, x),
            **prompt_kwargs,
        )

    def resolve_envvar_value(self, ctx: Context) -> str | None:
        """:class:`Option` resolves its environment variable the same way as
        :func:`Parameter.resolve_envvar_value`, but it also supports
        :attr:`Context.auto_envvar_prefix`. If we could not find an environment from
        the :attr:`envvar` property, we fallback on :attr:`Context.auto_envvar_prefix`
        to build dynamiccaly the environment variable name using the
        :python:`{ctx.auto_envvar_prefix}_{self.name.upper()}` template.

        :meta private:
        """
        rv = super().resolve_envvar_value(ctx)

        if rv is not None:
            return rv

        if (
            self.allow_from_autoenv
            and ctx.auto_envvar_prefix is not None
            and self.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"
            rv = os.environ.get(envvar)

            if rv:
                return rv

        return None

    def value_from_envvar(self, ctx: Context) -> t.Any:
        """For :class:`Option`, this method processes the raw environment variable
        string the same way as :func:`Parameter.value_from_envvar` does.

        But in the case of non-boolean flags, the value is analyzed to determine if the
        flag is activated or not, and returns a boolean of its activation, or the
        :attr:`flag_value` if the latter is set.

        This method also takes care of repeated options (i.e. options with
        :attr:`multiple` set to ``True``).

        :meta private:
        """
        rv = self.resolve_envvar_value(ctx)

        # Absent environment variable or an empty string is interpreted as unset.
        if rv is None:
            return None

        # Non-boolean flags are more liberal in what they accept. But a flag being a
        # flag, its envvar value still needs to be analyzed to determine if the flag is
        # activated or not.
        if self.is_flag and not self.is_bool_flag:
            # If the flag_value is set and match the envvar value, return it
            # directly.
            if self.flag_value is not UNSET and rv == self.flag_value:
                return self.flag_value
            # Analyze the envvar value as a boolean to know if the flag is
            # activated or not.
            return types.BoolParamType.str_to_bool(rv)

        # Split the envvar value if it is allowed to be repeated.
        value_depth = (self.nargs != 1) + bool(self.multiple)
        if value_depth > 0:
            multi_rv = self.type.split_envvar_value(rv)
            if self.multiple and self.nargs != 1:
                multi_rv = batch(multi_rv, self.nargs)  # type: ignore[assignment]

            return multi_rv

        return rv

    def consume_value(
        self, ctx: Context, opts: cabc.Mapping[str, Parameter]
    ) -> tuple[t.Any, ParameterSource]:
        """For :class:`Option`, the value can be collected from an interactive prompt
        if the option is a flag that needs a value (and the :attr:`prompt` property is
        set).

        Additionally, this method handles flag option that are activated without a
        value, in which case the :attr:`flag_value` is returned.

        :meta private:
        """
        value, source = super().consume_value(ctx, opts)

        # The parser will emit a sentinel value if the option is allowed to as a flag
        # without a value.
        if value is FLAG_NEEDS_VALUE:
            # If the option allows for a prompt, we start an interaction with the user.
            if self.prompt is not None and not ctx.resilient_parsing:
                value = self.prompt_for_value(ctx)
                source = ParameterSource.PROMPT
            # Else the flag takes its flag_value as value.
            else:
                value = self.flag_value
                source = ParameterSource.COMMANDLINE

        # A flag which is activated always returns the flag value, unless the value
        # comes from the explicitly sets default.
        elif (
            self.is_flag
            and value is True
            and not self.is_bool_flag
            and source not in (ParameterSource.DEFAULT, ParameterSource.DEFAULT_MAP)
        ):
            value = self.flag_value

        # Re-interpret a multiple option which has been sent as-is by the parser.
        # Here we replace each occurrence of value-less flags (marked by the
        # FLAG_NEEDS_VALUE sentinel) with the flag_value.
        elif (
            self.multiple
            and value is not UNSET
            and source not in (ParameterSource.DEFAULT, ParameterSource.DEFAULT_MAP)
            and any(v is FLAG_NEEDS_VALUE for v in value)
        ):
            value = [self.flag_value if v is FLAG_NEEDS_VALUE else v for v in value]
            source = ParameterSource.COMMANDLINE

        # The value wasn't set, or used the param's default, prompt for one to the user
        # if prompting is enabled.
        elif (
            (
                value is UNSET
                or source in (ParameterSource.DEFAULT, ParameterSource.DEFAULT_MAP)
            )
            and self.prompt is not None
            and (self.required or self.prompt_required)
            and not ctx.resilient_parsing
        ):
            value = self.prompt_for_value(ctx)
            source = ParameterSource.PROMPT

        return value, source

    def process_value(self, ctx: Context, value: t.Any) -> t.Any:
        # process_value has to be overridden on Options in order to capture
        # `value == UNSET` cases before `type_cast_value()` gets called.
        #
        # Refs:
        # https://github.com/pallets/click/issues/3069
        if self.is_flag and not self.required and self.is_bool_flag and value is UNSET:
            value = False

            if self.callback is not None:
                value = self.callback(ctx, self, value)

            return value

        # in the normal case, rely on Parameter.process_value
        return super().process_value(ctx, value)


class Argument(Parameter):
    """Arguments are positional parameters to a command.  They generally
    provide fewer features than options but can have infinite ``nargs``
    and are required by default.

    All parameters are passed onwards to the constructor of :class:`Parameter`.
    """

    param_type_name = "argument"

    def __init__(
        self,
        param_decls: cabc.Sequence[str],
        required: bool | None = None,
        **attrs: t.Any,
    ) -> None:
        # Auto-detect the requirement status of the argument if not explicitly set.
        if required is None:
            # The argument gets automatically required if it has no explicit default
            # value set and is setup to match at least one value.
            if attrs.get("default", UNSET) is UNSET:
                required = attrs.get("nargs", 1) > 0
            # If the argument has a default value, it is not required.
            else:
                required = False

        if "multiple" in attrs:
            raise TypeError("__init__() got an unexpected keyword argument 'multiple'.")

        super().__init__(param_decls, required=required, **attrs)

    @property
    def human_readable_name(self) -> str:
        if self.metavar is not None:
            return self.metavar
        return self.name.upper()  # type: ignore

    def make_metavar(self, ctx: Context) -> str:
        if self.metavar is not None:
            return self.metavar
        var = self.type.get_metavar(param=self, ctx=ctx)
        if not var:
            var = self.name.upper()  # type: ignore
        if self.deprecated:
            var += "!"
        if not self.required:
            var = f"[{var}]"
        if self.nargs != 1:
            var += "..."
        return var

    def _parse_decls(
        self, decls: cabc.Sequence[str], expose_value: bool
    ) -> tuple[str | None, list[str], list[str]]:
        if not decls:
            if not expose_value:
                return None, [], []
            raise TypeError("Argument is marked as exposed, but does not have a name.")
        if len(decls) == 1:
            name = arg = decls[0]
            name = name.replace("-", "_").lower()
        else:
            raise TypeError(
                "Arguments take exactly one parameter declaration, got"
                f" {len(decls)}: {decls}."
            )
        return name, [arg], []

    def get_usage_pieces(self, ctx: Context) -> list[str]:
        return [self.make_metavar(ctx)]

    def get_error_hint(self, ctx: Context) -> str:
        return f"'{self.make_metavar(ctx)}'"

    def add_to_parser(self, parser: _OptionParser, ctx: Context) -> None:
        parser.add_argument(dest=self.name, nargs=self.nargs, obj=self)
