# Code adapted from Click 8.3.1

from __future__ import annotations

from collections.abc import Callable, Iterator, MutableMapping
from contextlib import ExitStack, contextmanager
from threading import local
from types import TracebackType
from typing import (
    Any,
    Literal,
    NoReturn,
    TypeVar,
    cast,
    overload,
)

from . import _click
from .core import Parameter, TyperCommand

V = TypeVar("V")


class Context:
    """
    The [`Context`](https://click.palletsprojects.com/en/stable/api/#click.Context) has some additional data about the current execution of your program.
    When declaring it in a [callback](https://typer.tiangolo.com/tutorial/options/callback-and-context/) function,
    you can access this additional information.
    """

    formatter_class: type[_click.HelpFormatter] = _click.HelpFormatter

    def __init__(
        self,
        command: TyperCommand,
        parent: Context | None = None,
        info_name: str | None = None,
        obj: Any | None = None,
        auto_envvar_prefix: str | None = None,
        default_map: MutableMapping[str, Any] | None = None,
        terminal_width: int | None = None,
        max_content_width: int | None = None,
        resilient_parsing: bool = False,
        allow_extra_args: bool | None = None,
        allow_interspersed_args: bool | None = None,
        ignore_unknown_options: bool | None = None,
        help_option_names: list[str] | None = None,
        token_normalize_func: Callable[[str], str] | None = None,
        color: bool | None = None,
        show_default: bool | None = None,
    ) -> None:
        #: the parent context or `None` if none exists.
        self.parent = parent
        #: the :class:`Command` for this context.
        self.command = command
        #: the descriptive information name
        self.info_name = info_name
        #: Map of parameter names to their parsed values. Parameters
        #: with ``expose_value=False`` are not stored.
        self.params: dict[str, Any] = {}
        #: the leftover arguments.
        self.args: list[str] = []
        #: the collected prefixes of the command's options.
        self._opt_prefixes: set[str] = set(parent._opt_prefixes) if parent else set()

        if obj is None and parent is not None:
            obj = parent.obj

        #: the user object stored.
        self.obj: Any = obj
        self._meta: dict[str, Any] = getattr(parent, "meta", {})

        #: A dictionary (-like object) with defaults for parameters.
        if (
            default_map is None
            and info_name is not None
            and parent is not None
            and parent.default_map is not None
        ):
            default_map = parent.default_map.get(info_name)

        self.default_map: MutableMapping[str, Any] | None = default_map

        self.invoked_subcommand: str | None = None

        if terminal_width is None and parent is not None:
            terminal_width = parent.terminal_width

        #: The width of the terminal (None is autodetection).
        self.terminal_width: int | None = terminal_width

        if max_content_width is None and parent is not None:
            max_content_width = parent.max_content_width

        #: The maximum width of formatted content (None implies a sensible
        #: default which is 80 for most things).
        self.max_content_width: int | None = max_content_width

        if allow_extra_args is None:
            allow_extra_args = command.allow_extra_args

        #: Indicates if the context allows extra args or if it should
        #: fail on parsing.
        self.allow_extra_args = allow_extra_args

        if allow_interspersed_args is None:
            allow_interspersed_args = command.allow_interspersed_args

        #: Indicates if the context allows mixing of arguments and
        #: options or not.
        self.allow_interspersed_args: bool = allow_interspersed_args

        if ignore_unknown_options is None:
            ignore_unknown_options = command.ignore_unknown_options

        #: Instructs click to ignore options that a command does not
        #: understand and will store it on the context for later
        #: processing.  This is primarily useful for situations where you
        #: want to call into external programs.  Generally this pattern is
        #: strongly discouraged because it's not possibly to losslessly
        #: forward all arguments.
        self.ignore_unknown_options: bool = ignore_unknown_options

        if help_option_names is None:
            if parent is not None:
                help_option_names = parent.help_option_names
            else:
                help_option_names = ["--help"]

        #: The names for the help options.
        self.help_option_names: list[str] = help_option_names

        if token_normalize_func is None and parent is not None:
            token_normalize_func = parent.token_normalize_func

        # An optional normalization function for tokens.  This is
        # options, choices, commands etc.
        self.token_normalize_func: Callable[[str], str] | None = token_normalize_func

        # Indicates if resilient parsing is enabled.  In that case Click
        # will do its best to not cause any failures and default values
        # will be ignored. Useful for completion.
        self.resilient_parsing: bool = resilient_parsing

        # If there is no envvar prefix yet, but the parent has one and
        # the command on this level has a name, we can expand the envvar
        # prefix automatically.
        if auto_envvar_prefix is None:
            if (
                parent is not None
                and parent.auto_envvar_prefix is not None
                and self.info_name is not None
            ):
                auto_envvar_prefix = (
                    f"{parent.auto_envvar_prefix}_{self.info_name.upper()}"
                )
        else:
            auto_envvar_prefix = auto_envvar_prefix.upper()

        if auto_envvar_prefix is not None:
            auto_envvar_prefix = auto_envvar_prefix.replace("-", "_")

        self.auto_envvar_prefix: str | None = auto_envvar_prefix

        if color is None and parent is not None:
            color = parent.color

        # Controls if styling output is wanted or not.
        self.color: bool | None = color

        if show_default is None and parent is not None:
            show_default = parent.show_default

        # Show option default values when formatting help text.
        self.show_default: bool | None = show_default

        self._close_callbacks: list[Callable[[], Any]] = []
        self._depth = 0
        self._parameter_source: dict[str, _click.ParameterSource] = {}
        self._exit_stack = ExitStack()

    def __enter__(self) -> Context:
        self._depth += 1
        push_context(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        self._depth -= 1
        exit_result: bool | None = None
        if self._depth == 0:
            exit_result = self._close_with_exception_info(exc_type, exc_value, tb)
        pop_context()

        return exit_result

    @contextmanager
    def scope(self, cleanup: bool = True) -> Iterator[Context]:
        """This helper method can be used with the context object to promote
        it to the current thread local (see :func:`get_current_context`).
        The default behavior of this is to invoke the cleanup functions which
        can be disabled by setting `cleanup` to `False`.  The cleanup
        functions are typically used for things such as closing file handles.

        If the cleanup is intended the context object can also be directly
        used as a context manager.

        Example usage::

            with ctx.scope():
                assert get_current_context() is ctx

        This is equivalent::

            with ctx:
                assert get_current_context() is ctx
        """
        if not cleanup:
            self._depth += 1
        try:
            with self as rv:
                yield rv
        finally:
            if not cleanup:
                self._depth -= 1

    @property
    def meta(self) -> dict[str, Any]:
        """This is a dictionary which is shared with all the contexts
        that are nested.  It exists so that click utilities can store some
        state here if they need to.  It is however the responsibility of
        that code to manage this dictionary well.

        The keys are supposed to be unique dotted strings.  For instance
        module paths are a good choice for it.  What is stored in there is
        irrelevant for the operation of click.  However what is important is
        that code that places data here adheres to the general semantics of
        the system.
        """
        return self._meta

    def make_formatter(self) -> _click.HelpFormatter:
        """Creates the :class:`~click.HelpFormatter` for the help and
        usage output.

        To quickly customize the formatter class used without overriding
        this method, set the :attr:`formatter_class` attribute.
        """
        return self.formatter_class(
            width=self.terminal_width, max_width=self.max_content_width
        )

    def call_on_close(self, f: Callable[..., Any]) -> Callable[..., Any]:
        """Register a function to be called when the context tears down.

        This can be used to close resources opened during the script
        execution. Resources that support Python's context manager
        protocol which would be used in a ``with`` statement should be
        registered with :meth:`with_resource` instead.
        """
        return self._exit_stack.callback(f)

    def close(self) -> None:
        """Invoke all close callbacks"""
        self._close_with_exception_info(None, None, None)

    def _close_with_exception_info(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        """Unwind the exit stack by calling its :meth:`__exit__` providing the exception
        information to allow for exception handling by the various resources registered
        using :meth;`with_resource`
        """
        exit_result = self._exit_stack.__exit__(exc_type, exc_value, tb)
        # In case the context is reused, create a new exit stack.
        self._exit_stack = ExitStack()

        return exit_result

    @property
    def command_path(self) -> str:
        """The computed command path.  This is used for the ``usage``
        information on the help page.  It's automatically created by
        combining the info names of the chain of contexts to the root.
        """
        rv = ""
        if self.info_name is not None:
            rv = self.info_name
        if self.parent is not None:
            parent_command_path = [self.parent.command_path]

            if isinstance(self.parent.command, TyperCommand):
                for param in self.parent.command.get_params(self):
                    parent_command_path.extend(param.get_usage_pieces(self))

            rv = f"{' '.join(parent_command_path)} {rv}"
        return rv.lstrip()

    def find_root(self) -> Context:
        """Finds the outermost context."""
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def find_object(self, object_type: type[V]) -> V | None:
        """Finds the closest object of a given type."""
        node: Context | None = self

        while node is not None:
            if isinstance(node.obj, object_type):
                return node.obj

            node = node.parent

        return None

    def ensure_object(self, object_type: type[V]) -> V:
        """Like :meth:`find_object` but sets the innermost object to a
        new instance of `object_type` if it does not exist.
        """
        rv = self.find_object(object_type)
        if rv is None:
            self.obj = rv = object_type()
        return rv

    @overload
    def lookup_default(self, name: str, call: Literal[True] = True) -> Any | None: ...

    @overload
    def lookup_default(
        self, name: str, call: Literal[False] = ...
    ) -> Any | Callable[[], Any] | None: ...

    def lookup_default(self, name: str, call: bool = True) -> Any | None:
        """Get the default for a parameter from :attr:`default_map`."""
        if self.default_map is not None:
            value = self.default_map.get(name, _click.UNSET)

            if call and callable(value):
                return value()

            return value

        return _click.UNSET

    def fail(self, message: str) -> NoReturn:
        """Aborts the execution of the program with a specific error
        message.
        """
        raise _click.UsageError(message, self)

    def abort(self) -> NoReturn:
        """Aborts the script."""
        raise _click.Abort()

    def exit(self, code: int = 0) -> NoReturn:
        """Exits the application with a given exit code."""
        self.close()
        raise _click.Exit(code)

    def get_usage(self) -> str:
        """Helper method to get formatted usage string for the current
        context and command.
        """
        return self.command.get_usage(self)

    def get_help(self) -> str:
        """Helper method to get formatted help page for the current
        context and command.
        """
        return self.command.get_help(self)

    def _make_sub_context(self, command: TyperCommand) -> Context:
        """Create a new context of the same type as this context, but
        for a new command.

        :meta private:
        """
        return type(self)(command, info_name=command.name, parent=self)

    @overload
    def invoke(self, callback: Callable[..., V], /, *args: Any, **kwargs: Any) -> V: ...

    @overload
    def invoke(self, callback: TyperCommand, /, *args: Any, **kwargs: Any) -> Any: ...

    def invoke(
        self, callback: TyperCommand | Callable[..., V], /, *args: Any, **kwargs: Any
    ) -> Any | V:
        """Invokes a command callback in exactly the way it expects.  There
        are two ways to invoke this method:

        1.  the first argument can be a callback and all other arguments and
            keyword arguments are forwarded directly to the function.
        2.  the first argument is a click command object.  In that case all
            arguments are forwarded as well but proper click parameters
            (options and click arguments) must be keyword arguments and Click
            will fill in defaults.
        """
        if isinstance(callback, TyperCommand):
            other_cmd = callback

            if other_cmd.callback is None:
                raise TypeError(
                    "The given command does not have a callback that can be invoked."
                )
            else:
                callback = cast("Callable[..., V]", other_cmd.callback)

            ctx = self._make_sub_context(other_cmd)

            for param in other_cmd.params:
                if param.name not in kwargs and param.expose_value:
                    default_value = param.get_default(ctx)
                    # We explicitly hide the :attr:`UNSET` value to the user, as we
                    # choose to make it an implementation detail. And because ``invoke``
                    # has been designed as part of Click public API, we return ``None``
                    # instead. Refs:
                    # https://github.com/pallets/click/issues/3066
                    # https://github.com/pallets/click/issues/3065
                    # https://github.com/pallets/click/pull/3068
                    if default_value is _click.UNSET:
                        default_value = None
                    kwargs[param.name] = param.type_cast_value(  # type: ignore
                        ctx, default_value
                    )

            # Track all kwargs as params, so that forward() will pass
            # them on in subsequent calls.
            ctx.params.update(kwargs)
        else:
            ctx = self

        with augment_usage_errors(self):
            with ctx:
                return callback(*args, **kwargs)

    def forward(self, cmd: TyperCommand, /, *args: Any, **kwargs: Any) -> Any:
        """Similar to :meth:`invoke` but fills in default keyword
        arguments from the current context if the other command expects
        it.  This cannot invoke callbacks directly, only other commands.
        """
        # Can only forward to other commands, not direct callbacks.
        if not isinstance(cmd, TyperCommand):
            raise TypeError("Callback is not a command.")

        for param in self.params:
            if param not in kwargs:
                kwargs[param] = self.params[param]

        return self.invoke(cmd, *args, **kwargs)

    def set_parameter_source(self, name: str, source: _click.ParameterSource) -> None:
        """Set the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.
        """
        self._parameter_source[name] = source

    def get_parameter_source(self, name: str) -> _click.ParameterSource | None:
        """Get the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.

        This can be useful for determining when a user specified a value
        on the command line that is the same as the default value. It
        will be :attr:`~click.core.ParameterSource.DEFAULT` only if the
        value was actually taken from the default.
        """
        return self._parameter_source.get(name)


@contextmanager
def augment_usage_errors(
    ctx: Context, param: Parameter | None = None
) -> Iterator[None]:
    """Context manager that attaches extra information to exceptions."""
    try:
        yield
    except _click.BadParameter as e:
        if e.ctx is None:
            e.ctx = ctx
        if param is not None and e.param is None:
            e.param = param
        raise
    except _click.UsageError as e:
        if e.ctx is None:
            e.ctx = ctx
        raise


_local = local()


@overload
def get_current_context(silent: Literal[False] = False) -> Context: ...


@overload
def get_current_context(silent: bool = ...) -> Context | None: ...


def get_current_context(silent: bool = False) -> Context | None:
    """Returns the current click context."""
    try:
        return cast("Context", _local.stack[-1])
    except (AttributeError, IndexError) as e:
        if not silent:
            raise RuntimeError("There is no active click context.") from e

    return None


def push_context(ctx: Context) -> None:
    """Pushes a new context to the current stack."""
    _local.__dict__.setdefault("stack", []).append(ctx)


def pop_context() -> None:
    """Removes the top level from the stack."""
    _local.stack.pop()
