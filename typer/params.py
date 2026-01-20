from typing import TYPE_CHECKING, Annotated, Any, Callable, Optional, Union, overload

import click
from annotated_doc import Doc

from .models import ArgumentInfo, OptionInfo

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion


# Overload for Option created with custom type 'parser'
@overload
def Option(
    # Parameter
    default: Optional[Any] = ...,
    *param_decls: str,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, list[str]]] = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[list["click.shell_completion.CompletionItem"], list[str]],
        ]
    ] = None,
    autocompletion: Optional[Callable[..., Any]] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    # Custom type
    parser: Optional[Callable[[str], Any]] = None,
    # Option
    show_default: Union[bool, str] = True,
    prompt: Union[bool, str] = False,
    confirmation_prompt: bool = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    # TODO: remove is_flag and flag_value in a future release
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = True,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any: ...


# Overload for Option created with custom type 'click_type'
@overload
def Option(
    # Parameter
    default: Optional[Any] = ...,
    *param_decls: str,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, list[str]]] = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[list["click.shell_completion.CompletionItem"], list[str]],
        ]
    ] = None,
    autocompletion: Optional[Callable[..., Any]] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    # Custom type
    click_type: Optional[click.ParamType] = None,
    # Option
    show_default: Union[bool, str] = True,
    prompt: Union[bool, str] = False,
    confirmation_prompt: bool = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    # TODO: remove is_flag and flag_value in a future release
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = True,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any: ...


def Option(
    # Parameter
    default: Annotated[
        Optional[Any],
        Doc(
            """
            Usually, CLI options are optional and have a default value, passed on like this:

            **Example**

            ```python
            @app.command()
            def main(network: str = typer.Option("CNN")):
                print(f"Training neural network of type: {network}")
            ```

            Note that this usage is deprecated, and we recommend to use `Annotated` instead:
            ```
            @app.command()
            def main(network: Annotated[str, typer.Option()] = "CNN"):
                print(f"Hello {name}!")
            ```

            You can also use `...` ([Ellipsis](https://docs.python.org/3/library/constants.html#Ellipsis)) as the "default" value to clarify that this is a required CLI option.
            """
        ),
    ] = ...,
    *param_decls: Annotated[
        str,
        Doc(
            """
            Positional argument that defines how users can call this option on the command line.
            If not defined, Typer will automatically use the function parameter as default.
            See [the tutorial about CLI Option Names](https://typer.tiangolo.com/tutorial/options/name/) for more details.

            **Example**

            ```python
            @app.command()
            def main(user_name: Annotated[str, typer.Option("--name", "-n", "-u")]):
                print(f"Hello {user_name}")
            ```
            """
        ),
    ],
    callback: Annotated[
        Optional[Callable[..., Any]],
        Doc(
            """
            Add a callback to this option, to execute additional logic after the value was received from the terminal.
            See [the tutorial about callbacks](https://typer.tiangolo.com/tutorial/options/callback-and-context/) for more details.

            **Example**

            ```python
            def name_callback(value: str):
                if value != "Deadpool":
                    raise typer.BadParameter("Only Deadpool is allowed")
                return value

            @app.command()
            def main(name: Annotated[str | None, typer.Option(callback=name_callback)] = None):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    metavar: Annotated[
        Optional[str],
        Doc(
            """
            Customize the name displayed in the help text to represent this CLI option. Note that this doesn't influence the way the option must be called.

            **Example**

            ```python
            @app.command()
            def main(user: Annotated[str, typer.Option(metavar="User name")]):
                print(f"Hello {user}")
            ```
            """
        ),
    ] = None,
    expose_value: Annotated[
        bool,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.

            ---

            If this is `True` then the value is passed onwards to the command callback and stored on the context, otherwise it’s skipped.
            """
        ),
    ] = True,
    is_eager: Annotated[
        bool,
        Doc(
            """
            Set an option to "eager" to ensure it gets processed before other CLI parameters. This could be relevant when there are other parameters with callbacks that could exit the program early.
            For more information and an extended example, see the documentation [here](https://typer.tiangolo.com/tutorial/options/version/#fix-with-is_eager).
            """
        ),
    ] = False,
    envvar: Annotated[
        Optional[Union[str, list[str]]],
        Doc(
            """
            Configure an option to read a value from an environment variable if it is not provided in the command line as a CLI option.
            For more information, see the [documentation on Environment Variables](https://typer.tiangolo.com/tutorial/arguments/envvar/).

            **Example**

            ```python
            @app.command()
            def main(user: Annotated[str, typer.Option(envvar="AWESOME_PERSON")]):
                print(f"Hello {user}")
            ```
            """
        ),
    ] = None,
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Annotated[
        Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[list["click.shell_completion.CompletionItem"], list[str]],
            ]
        ],
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.
            It is however not fully functional, and will likely be removed in future versions.
            """
        ),
    ] = None,
    autocompletion: Annotated[
        Optional[Callable[..., Any]],
        Doc(
            """
            Provide a custom function that helps to autocomplete the values of this option.
            See [the tutorial on parameter autocompletion](https://typer.tiangolo.com/tutorial/options-autocompletion) for more details.

            **Example**

            ```python
            def name_complete():
                return ["Me", "Myself", "I"]

            @app.command()
            def main(name: Annotated[str, typer.Option(autocompletion=name_complete)] = "World"):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    default_factory: Annotated[
        Optional[Callable[[], Any]],
        Doc(
            """
            Provide a custom function that dynamically generates a [default](https://typer.tiangolo.com/tutorial/arguments/default) for this option.

            **Example**

            ```python
            def get_name():
                return random.choice(["Me", "Myself", "I"])

            @app.command()
            def main(name: Annotated[str, typer.Option(default_factory=get_name)]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    # Custom type
    parser: Annotated[
        Optional[Callable[[str], Any]],
        Doc(
            """
            Use your own custom types in Typer applications by defining a `parser` function that parses input into your own types:

            **Example**

            ```python
            class CustomClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<CustomClass: value={self.value}>"

            def my_parser(value: str):
                return CustomClass(value * 2)

            @app.command()
            def main(opt: Annotated[CustomClass, typer.Option(parser=my_parser)] = "Foo"):
                print(f"--opt is {opt}")
            ```
            """
        ),
    ] = None,
    click_type: Annotated[
        Optional[click.ParamType],
        Doc(
            """
            Define this parameter to use a [custom Click type](https://click.palletsprojects.com/en/stable/parameters/#implementing-custom-types) in your Typer applications.

            **Example**

            ```python
            class CustomClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<CustomClass: value={self.value}>"

            class CustomClassParser(click.ParamType):
                name = "CustomClass"

                def convert(self, value, param, ctx):
                    return CustomClass(value * 3)

            @app.command()
            def main(opt: Annotated[CustomClass, typer.Option(click_type=CustomClassParser())] = "Foo"):
                print(f"--opt is {opt}")
            ```
            """
        ),
    ] = None,
    # Option
    show_default: Annotated[
        Union[bool, str],
        Doc(
            """
            When set to `False`, don't show the default value of this argument in the [help text](https://typer.tiangolo.com/tutorial/options/help/).

            **Example**

            ```python
            @app.command()
            def main(fullname: Annotated[str, typer.Option(show_default=False)] = "Wade Wilson"):
                print(f"Hello {fullname}")
            ```
            """
        ),
    ] = True,
    prompt: Annotated[
        Union[bool, str],
        Doc(
            """
            When set to `True`, a prompt will appear to ask for a value if it was not provided:

            **Example**

            ```python
            @app.command()
            def main(name: str, lastname: Annotated[str, typer.Option(prompt=True)]):
                print(f"Hello {name} {lastname}")
            ```
            """
        ),
    ] = False,
    confirmation_prompt: bool = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    # TODO: remove is_flag and flag_value in a future release
    is_flag: Annotated[
        Optional[bool],
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.
            It is however not fully functional, and will likely be removed in future versions.
            """
        ),
    ] = None,
    flag_value: Annotated[
        Optional[Any],
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.
            It is however not fully functional, and will likely be removed in future versions.
            """
        ),
    ] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: Annotated[
        bool,
        Doc(
            """
            When an ["envvar"](https://typer.tiangolo.com/tutorial/arguments/envvar) is defined, prevent it from showing up in the help text:

            **Example**

            ```python
            @app.command()
            def main(user: Annotated[str, typer.Option(envvar="AWESOME_PERSON", show_envvar=False)]):
                print(f"Hello {user}")
            ```
            """
        ),
    ] = True,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any:
    return OptionInfo(
        # Parameter
        default=default,
        param_decls=param_decls,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        autocompletion=autocompletion,
        default_factory=default_factory,
        # Custom type
        parser=parser,
        click_type=click_type,
        # Option
        show_default=show_default,
        prompt=prompt,
        confirmation_prompt=confirmation_prompt,
        prompt_required=prompt_required,
        hide_input=hide_input,
        is_flag=is_flag,
        flag_value=flag_value,
        count=count,
        allow_from_autoenv=allow_from_autoenv,
        help=help,
        hidden=hidden,
        show_choices=show_choices,
        show_envvar=show_envvar,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
        # Rich settings
        rich_help_panel=rich_help_panel,
    )


# Overload for Argument created with custom type 'parser'
@overload
def Argument(
    # Parameter
    default: Optional[Any] = ...,
    *,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, list[str]]] = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[list["click.shell_completion.CompletionItem"], list[str]],
        ]
    ] = None,
    autocompletion: Optional[Callable[..., Any]] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    # Custom type
    parser: Optional[Callable[[str], Any]] = None,
    # TyperArgument
    show_default: Union[bool, str] = True,
    show_choices: bool = True,
    show_envvar: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any: ...


# Overload for Argument created with custom type 'click_type'
@overload
def Argument(
    # Parameter
    default: Optional[Any] = ...,
    *,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, list[str]]] = None,
    # Note that shell_complete is not fully supported and will be removed in future versions
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[list["click.shell_completion.CompletionItem"], list[str]],
        ]
    ] = None,
    autocompletion: Optional[Callable[..., Any]] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    # Custom type
    click_type: Optional[click.ParamType] = None,
    # TyperArgument
    show_default: Union[bool, str] = True,
    show_choices: bool = True,
    show_envvar: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any: ...


def Argument(
    # Parameter
    default: Annotated[
        Optional[Any],
        Doc(
            """
            By default, CLI arguments are required. However, by giving them a default value they become [optional](https://typer.tiangolo.com/tutorial/arguments/optional):

            **Example**

            ```python
            @app.command()
                def main(name: str = typer.Argument("World")):
                print(f"Hello {name}!")
            ```

            Note that this usage is deprecated, and we recommend to use `Annotated` instead:
            ```
            @app.command()
            def main(name: Annotated[str, typer.Argument()] = "World"):
                print(f"Hello {name}!")
            ```
            """
        ),
    ] = ...,
    *,
    callback: Annotated[
        Optional[Callable[..., Any]],
        Doc(
            """
            Add a callback to this argument, to execute additional logic with the value received from the terminal.
            See [the tutorial about callbacks](https://typer.tiangolo.com/tutorial/options/callback-and-context/) for more details.

            **Example**

            ```python
            def name_callback(value: str):
                if value != "Deadpool":
                    raise typer.BadParameter("Only Deadpool is allowed")
                return value

            @app.command()
            def main(name: Annotated[str | None, typer.Argument(callback=name_callback)] = None):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    metavar: Annotated[
        Optional[str],
        Doc(
            """
            Customize the name displayed in the help text to represent this CLI argument.
            By default, it will be the same name you declared, in uppercase.
            See [the tutorial about CLI Arguments with Help](https://typer.tiangolo.com/tutorial/arguments/help/#custom-help-name-metavar) for more details.

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(metavar="✨username✨")] = "World"):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    expose_value: Annotated[
        bool,
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.

            ---

            If this is `True` then the value is passed onwards to the command callback and stored on the context, otherwise it’s skipped.
            """
        ),
    ] = True,
    is_eager: Annotated[
        bool,
        Doc(
            """
            Set an argument to "eager" to ensure it gets processed before other CLI parameters. This could be relevant when there are other parameters with callbacks that could exit the program early.
            For more information and an extended example, see the documentation [here](https://typer.tiangolo.com/tutorial/options/version/#fix-with-is_eager).
            """
        ),
    ] = False,
    envvar: Annotated[
        Optional[Union[str, list[str]]],
        Doc(
            """
            Configure an argument to read a value from an environment variable if it is not provided in the command line as a CLI argument.
            For more information, see the [documentation on Environment Variables](https://typer.tiangolo.com/tutorial/arguments/envvar/).

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(envvar="AWESOME_NAME")] = "World"):
                print(f"Hello Mr. {name}")
            ```
            """
        ),
    ] = None,
    # TODO: Remove shell_complete in a future version (after 0.16.0)
    shell_complete: Annotated[
        Optional[
            Callable[
                [click.Context, click.Parameter, str],
                Union[list["click.shell_completion.CompletionItem"], list[str]],
            ]
        ],
        Doc(
            """
            **Note**: you probably shouldn't use this parameter, it is inherited from Click and supported for compatibility.
            It is however not fully functional, and will likely be removed in future versions.
            """
        ),
    ] = None,
    autocompletion: Annotated[
        Optional[Callable[..., Any]],
        Doc(
            """
            Provide a custom function that helps to autocomplete the values of this argument.
            See [the tutorial on parameter autocompletion](https://typer.tiangolo.com/tutorial/options-autocompletion) for more details.

            **Example**

            ```python
            def name_complete():
                return ["Me", "Myself", "I"]

            @app.command()
            def main(name: Annotated[str, typer.Argument(autocompletion=name_complete)] = "World"):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    default_factory: Annotated[
        Optional[Callable[[], Any]],
        Doc(
            """
            Provide a custom function that dynamically generates a [default](https://typer.tiangolo.com/tutorial/arguments/default) for this argument.

            **Example**

            ```python
            def get_name():
                return random.choice(["Me", "Myself", "I"])

            @app.command()
            def main(name: Annotated[str, typer.Argument(default_factory=get_name)]):
                print(f"Hello {name}")
            ```
            """
        ),
    ] = None,
    # Custom type
    parser: Annotated[
        Optional[Callable[[str], Any]],
        Doc(
            """
            Use your own custom types in Typer applications by defining a `parser` function that parses input into your own types:

            **Example**

            ```python
            class CustomClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<CustomClass: value={self.value}>"

            def my_parser(value: str):
                return CustomClass(value * 2)

            @app.command()
            def main(arg: Annotated[CustomClass, typer.Argument(parser=my_parser):
                print(f"arg is {arg}")
            ```
            """
        ),
    ] = None,
    click_type: Annotated[
        Optional[click.ParamType],
        Doc(
            """
            Define this parameter to use a [custom Click type](https://click.palletsprojects.com/en/stable/parameters/#implementing-custom-types) in your Typer applications.

            **Example**

            ```python
            class CustomClass:
                def __init__(self, value: str):
                    self.value = value

                def __str__(self):
                    return f"<CustomClass: value={self.value}>"

            class CustomClassParser(click.ParamType):
                name = "CustomClass"

                def convert(self, value, param, ctx):
                    return CustomClass(value * 3)

            @app.command()
            def main(arg: Annotated[CustomClass, typer.Argument(click_type=CustomClassParser())]):
                print(f"arg is {arg}")
            ```
            """
        ),
    ] = None,
    # TyperArgument
    show_default: Annotated[
        Union[bool, str],
        Doc(
            """
            When set to `False`, don't show the default value of this argument in the [help text](https://typer.tiangolo.com/tutorial/arguments/help/).

            **Example**

            ```python
            @app.command()
            def main(fullname: Annotated[str, typer.Argument(show_default=False)] = "Wade Wilson"):
                print(f"Hello {fullname}")
            ```
            """
        ),
    ] = True,
    show_choices: bool = True,
    show_envvar: Annotated[
        bool,
        Doc(
            """
            When an ["envvar"](https://typer.tiangolo.com/tutorial/arguments/envvar) is defined, prevent it from showing up in the help text:

            **Example**

            ```python
            @app.command()
            def main(name: Annotated[str, typer.Argument(envvar="AWESOME_NAME", show_envvar=False)] = "World"):
                print(f"Hello Mr. {name}")
            ```
            """
        ),
    ] = True,
    help: Optional[str] = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[list[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, type[str], type[bytes]] = None,
    # Rich settings
    rich_help_panel: Union[str, None] = None,
) -> Any:
    return ArgumentInfo(
        # Parameter
        default=default,
        # Arguments can only have one param declaration
        # it will be generated from the param name
        param_decls=None,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        autocompletion=autocompletion,
        default_factory=default_factory,
        # Custom type
        parser=parser,
        click_type=click_type,
        # TyperArgument
        show_default=show_default,
        show_choices=show_choices,
        show_envvar=show_envvar,
        help=help,
        hidden=hidden,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
        # Rich settings
        rich_help_panel=rich_help_panel,
    )
