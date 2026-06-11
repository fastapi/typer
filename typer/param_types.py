import os
import stat
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, ClassVar, Generic, TypeVar, cast
from uuid import UUID as UUIDType

from pydantic import BeforeValidator, TypeAdapter, ValidationError

from . import _click
from ._click import types
from ._click.shell_completion import CompletionItem
from ._click.types import _get_error_msg, build_type_adapter
from ._typing import is_literal_type, literal_values
from .models import (
    AnyType,
    FileBinaryRead,
    FileBinaryWrite,
    FileText,
    FileTextWrite,
    ParameterInfo,
)

ParamTypeValue = TypeVar("ParamTypeValue")


def lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool:
    return isinstance(cls, type) and issubclass(cls, class_or_tuple)


class TyperChoice(types.ParamType, Generic[ParamTypeValue]):
    name = "choice"

    def __init__(
        self, choices: Iterable[ParamTypeValue], case_sensitive: bool = True
    ) -> None:
        self.choices: Sequence[ParamTypeValue] = tuple(choices)
        self.case_sensitive = case_sensitive

    def _normalized_mapping(
        self, ctx: _click.Context | None = None
    ) -> Mapping[ParamTypeValue, str]:
        """
        Returns mapping where keys are the original choices and the values are
        the normalized values that are accepted via the command line.
        """
        return {
            choice: self.normalize_choice(
                choice=choice,
                ctx=ctx,
            )
            for choice in self.choices
        }

    def normalize_choice(
        self, choice: ParamTypeValue, ctx: _click.Context | None
    ) -> str:
        normed_value = str(choice.value) if isinstance(choice, Enum) else str(choice)

        if ctx is not None and ctx.token_normalize_func is not None:
            normed_value = ctx.token_normalize_func(normed_value)

        if not self.case_sensitive:
            normed_value = normed_value.casefold()

        return normed_value

    def get_metavar(self, param: _click.Parameter, ctx: _click.Context) -> str | None:
        if param.param_type_name == "option" and not param.show_choices:  # type: ignore
            choice_metavars = [
                types.convert_type(type(choice)).name.upper() for choice in self.choices
            ]
            choices_str = "|".join([*dict.fromkeys(choice_metavars)])
        else:
            choices_str = "|".join(
                [str(i) for i in self._normalized_mapping(ctx=ctx).values()]
            )

        # Use curly braces to indicate a required argument.
        if param.required and param.param_type_name == "argument":
            return f"{{{choices_str}}}"

        # Use square braces to indicate an option or optional argument.
        return f"[{choices_str}]"

    def get_missing_message(
        self, param: _click.Parameter, ctx: _click.Context | None
    ) -> str:
        """Message shown when no choice is passed."""
        choices = ",\n\t".join(self._normalized_mapping(ctx=ctx).values())
        return f"Choose from:\n\t{choices}"

    def _build_class_adapter(
        self, ctx: _click.Context | None
    ) -> TypeAdapter[ParamTypeValue]:
        normalized_mapping = self._normalized_mapping(ctx=ctx)

        def parse_choice(value: Any) -> ParamTypeValue:
            normed_value = self.normalize_choice(choice=value, ctx=ctx)
            for original, normalized in normalized_mapping.items():
                if normalized == normed_value:
                    return original
            raise ValueError(self.get_invalid_choice_message(value=value, ctx=ctx))

        return TypeAdapter(Annotated[Any, BeforeValidator(parse_choice)])

    def convert(
        self, value: Any, param: _click.Parameter | None, ctx: _click.Context | None
    ) -> ParamTypeValue:
        try:
            return self._build_class_adapter(ctx).validate_python(value)
        except ValidationError as exc:
            self.fail(_get_error_msg(exc), param=param, ctx=ctx)

    def get_invalid_choice_message(self, value: Any, ctx: _click.Context | None) -> str:
        """Get the error message when the given choice is invalid."""
        choices_str = ", ".join(map(repr, self._normalized_mapping(ctx=ctx).values()))
        return f"{value!r} is not one of {choices_str}."

    def __repr__(self) -> str:
        return f"Choice({list(self.choices)})"

    def _choice_as_str(self, choice: ParamTypeValue) -> str:
        if isinstance(choice, Enum):
            return str(choice.value)
        return str(choice)

    def shell_complete(
        self, ctx: _click.Context, param: _click.Parameter, incomplete: str
    ) -> list[CompletionItem]:
        """Complete choices that start with the incomplete value."""

        str_choices = map(self._choice_as_str, self.choices)

        if self.case_sensitive:
            matched = (c for c in str_choices if c.startswith(incomplete))
        else:
            incomplete = incomplete.lower()
            matched = (c for c in str_choices if c.lower().startswith(incomplete))

        return [CompletionItem(c) for c in matched]


class TyperPath(types.ParamType):
    envvar_list_splitter: ClassVar[str] = os.path.pathsep

    def __init__(
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: type[Any] | None = None,
    ):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.readable = readable
        self.writable = writable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = "file"
        elif self.dir_okay and not self.file_okay:
            self.name = "directory"
        else:
            self.name = "path"

    def _parse_path_value(
        self,
        value: Any,
        param: _click.Parameter | None,
        ctx: _click.Context | None,
    ) -> Any:
        if self.type is None or self.type is str or self.type is bytes:
            return value
        if isinstance(self.type, type) and issubclass(self.type, Path):
            if isinstance(value, self.type):
                return value
            if isinstance(value, (str, os.PathLike)):
                try:
                    return build_type_adapter(self.type).validate_python(value)
                except ValidationError as exc:
                    self.fail(_get_error_msg(exc), param, ctx)
        return value

    def coerce_path_result(
        self, value: str | os.PathLike[str]
    ) -> str | bytes | os.PathLike[str]:
        if self.type is not None and not isinstance(value, self.type):
            if (
                self.type is str
            ):  # pragma: no cover  # TODO: perhaps this branch can't be hit and should be removed
                return os.fsdecode(value)
            elif self.type is bytes:
                return os.fsencode(value)
            else:
                return cast("os.PathLike[str]", self.type(value))

        return value

    def convert(
        self,
        value: str | os.PathLike[str],
        param: _click.Parameter | None,
        ctx: _click.Context | None,
    ) -> str | bytes | os.PathLike[str]:
        rv = self._parse_path_value(value, param, ctx)

        is_dash = self.file_okay and self.allow_dash and rv in (b"-", "-")

        if not is_dash:
            if self.resolve_path:
                rv = os.path.realpath(rv)

            try:
                st = os.stat(rv)
            except OSError:
                if not self.exists:
                    return self.coerce_path_result(rv)
                self.fail(
                    f"{self.name.title()} {_click.utils.format_filename(value)!r} does not exist.",
                    param,
                    ctx,
                )

            name = self.name.title()
            loc = repr(_click.utils.format_filename(value))
            if not self.file_okay and stat.S_ISREG(st.st_mode):
                self.fail(f"{name} {loc} is a file.", param, ctx)

            if not self.dir_okay and stat.S_ISDIR(st.st_mode):
                self.fail(f"{name} {loc} is a directory.", param, ctx)

            if self.readable and not os.access(rv, os.R_OK):
                self.fail(f"{name} {loc} is not readable.", param, ctx)

            if self.writable and not os.access(rv, os.W_OK):
                self.fail(f"{name} {loc} is not writable.", param, ctx)

        return self.coerce_path_result(rv)

    def shell_complete(
        self, ctx: _click.Context, param: _click.Parameter, incomplete: str
    ) -> list[CompletionItem]:
        """Return an empty list so that the autocompletion functionality
        will work properly from the commandline.
        """
        return []


def _file_param_type(parameter_info: ParameterInfo, *, mode: str) -> types.File:
    return types.File(
        mode=parameter_info.mode or mode,
        encoding=parameter_info.encoding,
        errors=parameter_info.errors,
        lazy=parameter_info.lazy,
        atomic=parameter_info.atomic,
    )


def _ranged_number_param_type(
    number_class: type[Any],
    *,
    min: int | float | None,
    max: int | float | None,
    clamp: bool,
) -> types.ParamType:
    return types.PydanticParamType(
        types.build_type_adapter(number_class, min=min, max=max, clamp=clamp),
        name="integer range" if number_class is int else "float range",
    )


def _needs_typer_path(annotation: Any, parameter_info: ParameterInfo) -> bool:
    return (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type is not None
        or parameter_info.resolve_path
    )


def get_param_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> types.ParamType:
    if parameter_info.parser is not None:
        return types.FuncParamType(parameter_info.parser)

    param_type = param_type_from_annotation(annotation, parameter_info)
    if param_type is not None:
        return param_type

    raise RuntimeError(f"Type not yet supported: {annotation}")  # pragma: no cover


def param_type_from_annotation(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> types.ParamType | None:
    if annotation is int or annotation is float:
        if parameter_info.min is not None or parameter_info.max is not None:
            min_ = parameter_info.min
            max_ = parameter_info.max
            if annotation is int:
                min_ = int(min_) if min_ is not None else None
                max_ = int(max_) if max_ is not None else None
            return _ranged_number_param_type(
                annotation,
                min=min_,
                max=max_,
                clamp=parameter_info.clamp,
            )
        return types.INT if annotation is int else types.FLOAT
    if annotation is UUIDType:
        return types.UUID
    if annotation is datetime:
        return types.datetime_param_type(formats=parameter_info.formats)
    if annotation is bool:
        return types.BOOL
    if _needs_typer_path(annotation, parameter_info):
        resolved_path_type: type[Any] | None = parameter_info.path_type
        if resolved_path_type is None and lenient_issubclass(annotation, Path):
            resolved_path_type = annotation
        return TyperPath(
            exists=parameter_info.exists,
            file_okay=parameter_info.file_okay,
            dir_okay=parameter_info.dir_okay,
            writable=parameter_info.writable,
            readable=parameter_info.readable,
            resolve_path=parameter_info.resolve_path,
            allow_dash=parameter_info.allow_dash,
            path_type=resolved_path_type,
        )
    if lenient_issubclass(annotation, Enum):
        return TyperChoice(
            list(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if is_literal_type(annotation):
        return TyperChoice(
            literal_values(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if annotation is str:
        return types.STRING
    if lenient_issubclass(annotation, FileTextWrite):
        return _file_param_type(parameter_info, mode="w")
    if lenient_issubclass(annotation, FileText):
        return _file_param_type(parameter_info, mode="r")
    if lenient_issubclass(annotation, FileBinaryRead):
        return _file_param_type(parameter_info, mode="rb")
    if lenient_issubclass(annotation, FileBinaryWrite):
        return _file_param_type(parameter_info, mode="wb")
    return None
