from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import UUID

import click
import pytest
from typer.main import get_click_type
from typer.models import FileBinaryRead, FileTextWrite, ParameterInfo
from typing_extensions import TypeAliasType


def test_get_click_type_with_custom_click_type():
    custom_click_type = click.INT
    param_info = ParameterInfo(click_type=custom_click_type)
    result = get_click_type(annotation=int, parameter_info=param_info)
    assert result is custom_click_type


def test_get_click_type_with_custom_parser():
    def mock_parser(x):
        return 42

    param_info = ParameterInfo(parser=mock_parser)
    result = get_click_type(annotation=int, parameter_info=param_info)
    assert isinstance(result, click.types.FuncParamType)
    assert result.convert("42", None, None) == 42


def test_get_click_type_with_str_annotation():
    param_info = ParameterInfo()
    result = get_click_type(annotation=str, parameter_info=param_info)
    assert result is click.STRING


def test_get_click_type_with_int_annotation_no_min_max():
    param_info = ParameterInfo()
    result = get_click_type(annotation=int, parameter_info=param_info)
    assert result is click.INT


def test_get_click_type_with_int_annotation_with_min_max():
    param_info = ParameterInfo(min=10, max=100)
    result = get_click_type(annotation=int, parameter_info=param_info)
    assert isinstance(result, click.IntRange)
    assert result.min == 10
    assert result.max == 100


def test_get_click_type_with_float_annotation_no_min_max():
    param_info = ParameterInfo()
    result = get_click_type(annotation=float, parameter_info=param_info)
    assert result is click.FLOAT


def test_get_click_type_with_float_annotation_with_min_max():
    param_info = ParameterInfo(min=0.1, max=10.5)
    result = get_click_type(annotation=float, parameter_info=param_info)
    assert isinstance(result, click.FloatRange)
    assert result.min == 0.1
    assert result.max == 10.5


def test_get_click_type_with_bool_annotation():
    param_info = ParameterInfo()
    result = get_click_type(annotation=bool, parameter_info=param_info)
    assert result is click.BOOL


def test_get_click_type_with_uuid_annotation():
    param_info = ParameterInfo()
    result = get_click_type(annotation=UUID, parameter_info=param_info)
    assert result is click.UUID


def test_get_click_type_with_datetime_annotation():
    param_info = ParameterInfo(formats=["%Y-%m-%d"])
    result = get_click_type(annotation=datetime, parameter_info=param_info)
    assert isinstance(result, click.DateTime)
    assert result.formats == ["%Y-%m-%d"]


def test_get_click_type_with_path_annotation():
    param_info = ParameterInfo(resolve_path=True)
    result = get_click_type(annotation=Path, parameter_info=param_info)
    assert isinstance(result, click.Path)
    assert result.resolve_path is True


def test_get_click_type_with_enum_annotation():
    class Color(Enum):
        RED = "red"
        BLUE = "blue"

    param_info = ParameterInfo()
    result = get_click_type(annotation=Color, parameter_info=param_info)
    assert isinstance(result, click.Choice)
    assert result.choices == ["red", "blue"]


def test_get_click_type_with_file_text_write_annotation():
    param_info = ParameterInfo(mode="w", encoding="utf-8")
    result = get_click_type(annotation=FileTextWrite, parameter_info=param_info)
    assert isinstance(result, click.File)
    assert result.mode == "w"
    assert result.encoding == "utf-8"


def test_get_click_type_with_file_binary_read_annotation():
    param_info = ParameterInfo(mode="rb")
    result = get_click_type(annotation=FileBinaryRead, parameter_info=param_info)
    assert isinstance(result, click.File)
    assert result.mode == "rb"


def test_get_click_type_with_type_alias_type():
    # define TypeAliasType
    Name = TypeAliasType(name="Name", value=str)
    Surname = TypeAliasType(name="Surname", value=Name)

    param_info = ParameterInfo()
    result = get_click_type(annotation=Name, parameter_info=param_info)
    assert result is click.STRING

    # recursive types
    param_info = ParameterInfo()
    result = get_click_type(annotation=Surname, parameter_info=param_info)
    assert result is click.STRING


def test_get_click_type_with_unsupported_type():
    class UnsupportedType:
        pass

    param_info = ParameterInfo()
    with pytest.raises(
        RuntimeError, match="Type not yet supported: <class '.*UnsupportedType.*'>"
    ):
        get_click_type(annotation=UnsupportedType, parameter_info=param_info)
