import inspect
from datetime import datetime
from enum import Enum
from functools import update_wrapper
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union
from uuid import UUID

import click

from .models import (
    AnyType,
    ArgumentInfo,
    BinaryFileRead,
    BinaryFileWrite,
    CommandFunctionType,
    CommandInfo,
    Default,
    DefaultPlaceholder,
    NoneType,
    OptionInfo,
    ParameterInfo,
    Required,
    TextFile,
    TyperInfo,
)


class Typer:
    def __init__(
        self,
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: Optional[bool] = Default(None),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
    ):
        self.info = TyperInfo(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
        )
        self.registered_groups: List[TyperInfo] = []
        self.registered_commands: List[CommandInfo] = []
        self.registered_callback: Optional[TyperInfo] = None

    def callback(
        self,
        name: Optional[str] = Default(None),
        *,
        cls: Optional[Type[click.Command]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: Optional[bool] = Default(None),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            self.registered_callback = TyperInfo(
                name=name,
                cls=cls,
                invoke_without_command=invoke_without_command,
                no_args_is_help=no_args_is_help,
                subcommand_metavar=subcommand_metavar,
                chain=chain,
                result_callback=result_callback,
                context_settings=context_settings,
                callback=f,
                help=help,
                epilog=epilog,
                short_help=short_help,
                options_metavar=options_metavar,
                add_help_option=add_help_option,
                hidden=hidden,
                deprecated=deprecated,
            )
            return f

        return decorator

    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[click.Command]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        if cls is None:
            cls = click.Command

        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            self.registered_commands.append(
                CommandInfo(
                    name=name,
                    cls=cls,
                    context_settings=context_settings,
                    callback=f,
                    help=help,
                    epilog=epilog,
                    short_help=short_help,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    hidden=hidden,
                    deprecated=deprecated,
                )
            )
            return f

        return decorator

    def add_typer(
        self,
        typer_instance: "Typer",
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: Optional[bool] = Default(None),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
    ) -> None:
        self.registered_groups.append(
            TyperInfo(
                typer_instance,
                name=name,
                cls=cls,
                invoke_without_command=invoke_without_command,
                no_args_is_help=no_args_is_help,
                subcommand_metavar=subcommand_metavar,
                chain=chain,
                result_callback=result_callback,
                context_settings=context_settings,
                callback=callback,
                help=help,
                epilog=epilog,
                short_help=short_help,
                options_metavar=options_metavar,
                add_help_option=add_help_option,
                hidden=hidden,
                deprecated=deprecated,
            )
        )

    def __call__(self) -> Any:
        return get_command(self)()


def get_group(typer_instance: Typer) -> click.Command:
    group = get_group_from_info(TyperInfo(typer_instance))
    return group


def get_command(typer_instance: Typer) -> click.Command:
    if (
        typer_instance.registered_callback
        or typer_instance.registered_groups
        or len(typer_instance.registered_commands) > 1
    ):
        return get_group(typer_instance)
    elif len(typer_instance.registered_commands) == 1:
        return get_command_from_info(typer_instance.registered_commands[0])
    assert False, "Could not get a command for this Typer instance"


def get_group_name(typer_info: TyperInfo) -> str:
    if typer_info.callback:
        # Priority 1: Callback passed in app.add_typer()
        return get_command_name(typer_info.callback.__name__)
    if typer_info.typer_instance:
        registered_callback = typer_info.typer_instance.registered_callback
        if registered_callback:
            if registered_callback.callback:
                # Priority 2: Callback passed in @subapp.callback()
                return get_command_name(registered_callback.callback.__name__)
        if typer_info.typer_instance.info.callback:
            return get_command_name(typer_info.typer_instance.info.callback.__name__)
    assert False, "A Group name could not be created"


def solve_typer_info_defaults(typer_info: TyperInfo) -> TyperInfo:
    values = {}
    name = None
    for name, value in typer_info.__dict__.items():
        # Priority 1: Value was set in app.add_typer()
        if not isinstance(value, DefaultPlaceholder):
            values[name] = value
            continue
        if typer_info.typer_instance:
            if typer_info.typer_instance.registered_callback:
                callback_value = getattr(
                    typer_info.typer_instance.registered_callback, name
                )
                # Priority 2: Value was set in @subapp.callback()
                if not isinstance(callback_value, DefaultPlaceholder):
                    values[name] = callback_value
                    continue
            instance_value = getattr(typer_info.typer_instance.info, name)
            # Priority 3: Value set in subapp = typer.Typer()
            if not isinstance(instance_value, DefaultPlaceholder):
                values[name] = instance_value
                continue
        # Value not set, use the default
        values[name] = value.value
    if values["name"] is None:
        values["name"] = get_group_name(typer_info)
    return TyperInfo(**values)


def get_group_from_info(group_info: TyperInfo) -> click.Command:
    assert (
        group_info.typer_instance
    ), "A Typer instance is needed to generate a Click Group"
    commands: Dict[str, click.Command] = {}
    for command_info in group_info.typer_instance.registered_commands:
        command = get_command_from_info(command_info=command_info)
        commands[command.name] = command
    for sub_group_info in group_info.typer_instance.registered_groups:
        sub_group = get_group_from_info(sub_group_info)
        commands[sub_group.name] = sub_group
    solved_info = solve_typer_info_defaults(group_info)
    (
        params,
        convertors,
        context_param_name,
    ) = get_params_convertors_ctx_param_name_from_function(solved_info.callback)
    cls = solved_info.cls or click.Group
    group = cls(  # type: ignore
        name=solved_info.name or "",
        commands=commands,
        invoke_without_command=solved_info.invoke_without_command,
        no_args_is_help=solved_info.no_args_is_help,
        subcommand_metavar=solved_info.subcommand_metavar,
        chain=solved_info.chain,
        result_callback=solved_info.result_callback,
        context_settings=solved_info.context_settings,
        callback=get_callback(
            callback=solved_info.callback,
            params=params,
            convertors=convertors,
            context_param_name=context_param_name,
        ),
        params=params,  # type: ignore
        help=solved_info.help,
        epilog=solved_info.epilog,
        short_help=solved_info.short_help,
        options_metavar=solved_info.options_metavar,
        add_help_option=solved_info.add_help_option,
        hidden=solved_info.hidden,
        deprecated=solved_info.deprecated,
    )
    return group


def get_command_name(name: str) -> str:
    return name.lower().replace("_", "-")


def get_params_convertors_ctx_param_name_from_function(
    callback: Optional[Callable[..., Any]]
) -> Tuple[List[Union[click.Argument, click.Option]], Dict[str, Any], Optional[str]]:
    params = []
    convertors = {}
    context_param_name = None
    if callback:
        signature = inspect.signature(callback)
        for param_name, param in signature.parameters.items():
            if lenient_issubclass(param.annotation, click.Context):
                context_param_name = param_name
                continue
            click_param, convertor = get_click_param(param)
            if convertor:
                convertors[param_name] = convertor
            params.append(click_param)
    return params, convertors, context_param_name


def get_command_from_info(command_info: CommandInfo) -> click.Command:
    assert command_info.callback, "A command must have a callback function"
    name = command_info.name or get_command_name(command_info.callback.__name__)
    (
        params,
        convertors,
        context_param_name,
    ) = get_params_convertors_ctx_param_name_from_function(command_info.callback)
    cls = command_info.cls or click.Command
    command = cls(  # type: ignore
        name=name,
        context_settings=command_info.context_settings,
        callback=get_callback(
            callback=command_info.callback,
            params=params,
            convertors=convertors,
            context_param_name=context_param_name,
        ),
        params=params,  # type: ignore
        help=command_info.help,
        epilog=command_info.epilog,
        short_help=command_info.short_help,
        options_metavar=command_info.options_metavar,
        add_help_option=command_info.add_help_option,
        hidden=command_info.hidden,
        deprecated=command_info.deprecated,
    )
    return command


def param_path_convertor(value: Optional[str] = None) -> Optional[Path]:
    if value is not None:
        return Path(value)
    return None


def generate_enum_convertor(enum: Type[Enum]) -> Callable:
    lower_val_map = {str(val.value).lower(): val for val in enum}

    def convertor(value: Any) -> Any:
        if value is not None:
            low = str(value).lower()
            if low in lower_val_map:
                key = lower_val_map[low]
                return enum(key)

    return convertor


def get_callback(
    *,
    callback: Optional[Callable] = None,
    params: Sequence[click.Parameter] = [],
    convertors: Dict[str, Callable[[str], Any]] = {},
    context_param_name: str = None,
) -> Optional[Callable]:
    if not callback:
        return None
    signature = inspect.signature(callback)
    use_params: Dict[str, Any] = {}
    for param_name, param_sig in signature.parameters.items():
        use_params[param_name] = None
    for param in params:
        use_params[param.name] = param.default

    def wrapper(**kwargs: Any) -> Any:
        for k, v in kwargs.items():
            if k in convertors:
                use_params[k] = convertors[k](v)
            else:
                use_params[k] = v
        if context_param_name:
            use_params[context_param_name] = click.get_current_context()
        return callback(**use_params)  # type: ignore

    update_wrapper(wrapper, callback)
    return wrapper


def get_click_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> click.ParamType:
    if annotation == str:
        return click.STRING
    elif annotation == int:
        if parameter_info.min is not None or parameter_info.max is not None:
            min_ = None
            max_ = None
            if parameter_info.min is not None:
                min_ = int(parameter_info.min)
            if parameter_info.max is not None:
                max_ = int(parameter_info.max)
            return click.IntRange(min=min_, max=max_, clamp=parameter_info.clamp,)
        else:
            return click.INT
    elif annotation == float:
        if parameter_info.min is not None or parameter_info.max is not None:
            return click.FloatRange(
                min=parameter_info.min,
                max=parameter_info.max,
                clamp=parameter_info.clamp,
            )
        else:
            return click.FLOAT
    elif annotation == bool:
        return click.BOOL
    elif annotation == UUID:
        return click.UUID
    elif annotation == datetime:
        return click.DateTime(formats=parameter_info.formats)
    elif (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type
        or parameter_info.resolve_path
    ):
        return click.Path(  # type: ignore
            exists=parameter_info.exists,
            file_okay=parameter_info.file_okay,
            dir_okay=parameter_info.dir_okay,
            writable=parameter_info.writable,
            readable=parameter_info.readable,
            resolve_path=parameter_info.resolve_path,
            allow_dash=parameter_info.allow_dash,
            path_type=parameter_info.path_type,
        )
    elif lenient_issubclass(annotation, TextFile):
        return click.File(
            mode=parameter_info.mode or "r",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, BinaryFileRead):
        return click.File(
            mode=parameter_info.mode or "rb",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, BinaryFileWrite):
        return click.File(
            mode=parameter_info.mode or "wb",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, Enum):
        return click.Choice(
            [item.value for item in annotation],
            case_sensitive=parameter_info.case_sensitive,
        )
    raise RuntimeError(f"Type not yet supported: {annotation}")


def lenient_issubclass(
    cls: Any, class_or_tuple: Union[AnyType, Tuple[AnyType, ...]]
) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


def get_click_param(
    param: inspect.Parameter,
) -> Tuple[Union[click.Argument, click.Option], Any]:
    # First, find out what will be:
    # * ParamInfo (ArgumentInfo or OptionInfo)
    # * default_value
    # * required
    default_value = None
    required = False
    if isinstance(param.default, ParameterInfo):
        parameter_info = param.default
        if parameter_info.default == Required:
            required = True
        else:
            default_value = parameter_info.default
    elif param.default == Required or param.default == param.empty:
        required = True
        parameter_info = ArgumentInfo()
    else:
        default_value = param.default
        parameter_info = OptionInfo()
    annotation: Any = Any
    if not param.annotation == param.empty:
        annotation = param.annotation
    else:
        annotation = str
    main_type = annotation
    is_list = False
    parameter_type: Any = None
    is_flag = None
    origin = getattr(main_type, "__origin__", None)
    if origin is not None:
        # Handle Optional[SomeType]
        if origin is Union:
            types = []
            for type_ in main_type.__args__:
                if type_ is NoneType:  # type: ignore
                    continue
                types.append(type_)
            assert len(types) == 1, "Typer Currently doesn't support Union types"
            main_type = types[0]
            origin = getattr(main_type, "__origin__", None)
        # Handle Tuples and Lists
        if lenient_issubclass(origin, List):
            main_type = main_type.__args__[0]
            assert (
                "__origin__" not in main_type
            ), "List types with complex sub-types are not currently supported"
            is_list = True
        elif lenient_issubclass(origin, Tuple):  # type: ignore
            types = []
            for type_ in origin.__args__:
                assert (
                    "__origin__" not in type_
                ), "Tuple types with complex sub-types are not currently supported"
                types.append(
                    get_click_type(annotation=type_, parameter_info=parameter_info)
                )
            parameter_type = tuple(types)
    if parameter_type is None:
        parameter_type = get_click_type(
            annotation=main_type, parameter_info=parameter_info
        )
    convertor = None
    if lenient_issubclass(main_type, Path):
        convertor = param_path_convertor
    if lenient_issubclass(main_type, Enum):
        convertor = generate_enum_convertor(main_type)
    if isinstance(parameter_info, OptionInfo):
        if main_type is bool and not (parameter_info.is_flag is False):
            is_flag = True
            # Click doesn't accept a flag of type bool, only None, and then it sets it
            # to bool internally
            parameter_type = None
        default_option_name = get_command_name(param.name)
        if is_flag:
            default_option_declaration = (
                f"--{default_option_name}/--no-{default_option_name}"
            )
        else:
            default_option_declaration = f"--{default_option_name}"
        param_decls = [param.name]
        if parameter_info.param_decls:
            param_decls.extend(parameter_info.param_decls)
        else:
            param_decls.append(default_option_declaration)
        return (
            click.Option(
                # Option
                param_decls=param_decls,
                show_default=parameter_info.show_default,
                prompt=parameter_info.prompt,
                confirmation_prompt=parameter_info.confirmation_prompt,
                hide_input=parameter_info.hide_input,
                is_flag=is_flag,
                flag_value=parameter_info.flag_value,
                multiple=is_list,
                count=parameter_info.count,
                allow_from_autoenv=parameter_info.allow_from_autoenv,
                type=parameter_type,
                help=parameter_info.help,
                hidden=parameter_info.hidden,
                show_choices=parameter_info.show_choices,
                show_envvar=parameter_info.show_envvar,
                # Parameter
                required=required,
                default=default_value,
                callback=parameter_info.callback,
                metavar=parameter_info.metavar,
                expose_value=parameter_info.expose_value,
                is_eager=parameter_info.is_eager,
                envvar=parameter_info.envvar,
                autocompletion=parameter_info.autocompletion,
            ),
            convertor,
        )
    elif isinstance(parameter_info, ArgumentInfo):
        param_decls = [param.name]
        if parameter_info.param_decls:
            param_decls.extend(parameter_info.param_decls)
        nargs = None
        if is_list:
            nargs = -1
        return (
            click.Argument(
                # Argument
                param_decls=param_decls,
                type=parameter_type,
                required=required,
                nargs=nargs,
                # Parameter
                default=default_value,
                callback=parameter_info.callback,
                metavar=parameter_info.metavar,
                expose_value=parameter_info.expose_value,
                is_eager=parameter_info.is_eager,
                envvar=parameter_info.envvar,
                autocompletion=parameter_info.autocompletion,
            ),
            convertor,
        )
    assert False, "A click.Parameter should be returned"


def run(function: Callable) -> Any:
    app = Typer()
    app.command()(function)
    app()
