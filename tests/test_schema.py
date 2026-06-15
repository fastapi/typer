from enum import Enum
from pathlib import Path
from typing import Any

import pytest
import typer
from typer.adapters import build_adapter
from typer.main import get_command
from typer.param_types import choice_coercion_annotation, file_coercion_annotation
from typer.schema import ChoiceRuntimeParam, FileRuntimeParam
from typer.testing import CliRunner

runner = CliRunner()


def test_simple_command_schema() -> None:
    app = typer.Typer()

    @app.command()
    def main(name: str, age: int = 0, active: bool = False):
        pass

    schema = get_command(app).schema
    assert [param.name for param in schema.params] == ["name", "age", "active"]

    name_param = schema.get_param("name")
    assert name_param is not None
    assert name_param.annotation is str
    assert name_param.kind == "argument"
    assert name_param.required is True

    age_param = schema.get_param("age")
    assert age_param is not None
    assert age_param.annotation is int
    assert age_param.kind == "option"
    assert age_param.default == 0

    active_param = schema.get_param("active")
    assert active_param is not None
    assert active_param.is_flag is True
    assert active_param.is_bool_flag is True


@pytest.mark.parametrize(
    ("raw", "expected", "expected_type"),
    [
        ("42", 42, int),
        ("3.5", 3.5, float),
        ("hello", "hello", str),
        (True, True, bool),
    ],
)
def test_schema_coerce_scalars(raw: Any, expected: Any, expected_type: type) -> None:
    adapter = build_adapter(expected_type, typer.models.OptionInfo())
    runtime_value = adapter.validate_python(raw)

    assert runtime_value == expected
    assert type(runtime_value) is expected_type


def test_schema_coerce_list() -> None:
    app = typer.Typer()

    @app.command()
    def main(items: list[int]):
        pass

    schema = get_command(app).schema
    runtime_param = schema.get_param("items")
    assert runtime_param is not None
    assert runtime_param.annotation == list[int]
    assert runtime_param.multiple is True

    assert runtime_param.coerce(("1", "2", "3")) == [1, 2, 3]


def test_schema_coerce_enum() -> None:
    class Color(str, Enum):
        RED = "red"
        BLUE = "blue"

    app = typer.Typer()

    @app.command()
    def main(color: Color):
        pass

    schema = get_command(app).schema
    runtime_param = schema.get_param("color")
    assert runtime_param is not None
    assert isinstance(runtime_param, ChoiceRuntimeParam)
    assert runtime_param.coerce("red") is Color.RED


def test_schema_coerce_unannotated_default() -> None:
    app = typer.Typer()

    @app.command()
    def main(val=42):
        pass

    schema = get_command(app).schema
    runtime_param = schema.get_param("val")
    assert runtime_param is not None
    assert runtime_param.annotation is int
    assert runtime_param.coerce("99") == 99


def test_runtime_coercion_on_invoke() -> None:
    app = typer.Typer()
    seen: dict[str, Any] = {}

    @app.command()
    def main(
        items: list[int],
        active: bool = False,
        val=42,
    ):
        seen["items"] = items
        seen["active"] = active
        seen["val"] = val

    result = runner.invoke(app, ["1", "2", "--active", "--val", "7"])
    assert result.exit_code == 0, result.output
    assert seen == {"items": [1, 2], "active": True, "val": 7}
    assert all(isinstance(v, int) for v in seen["items"])
    assert isinstance(seen["val"], int)


def test_runtime_coercion_invalid_value() -> None:
    app = typer.Typer()

    @app.command()
    def main(age: int):
        pass

    result = runner.invoke(app, ["--age", "not-an-int"])
    assert result.exit_code != 0


def test_schema_coerce_command_values() -> None:
    app = typer.Typer()
    seen: dict[str, Any] = {}

    @app.command()
    def main(name: str, count: int = 1):
        seen["name"] = name
        seen["count"] = count

    schema = get_command(app).schema
    coerced = schema.coerce({"name": "Ada", "count": "3"})
    assert coerced == {"name": "Ada", "count": 3}

    result = runner.invoke(app, ["Ada", "--count", "3"])
    assert result.exit_code == 0
    assert seen == {"name": "Ada", "count": 3}


@pytest.mark.parametrize(
    ("annotation", "expected"),
    [
        (typer.FileText, typer.FileText),
        (list[typer.FileText], typer.FileText),
        (tuple[typer.FileText], typer.FileText),
        (tuple[typer.FileText, typer.FileTextWrite], typer.FileText),
        (tuple[typer.FileText, str], None),
        (tuple[str, str], None),
    ],
)
def test_file_coercion_annotation(annotation: Any, expected: Any) -> None:
    assert file_coercion_annotation(annotation) is expected


def test_choice_coercion_annotation() -> None:
    class Color(str, Enum):
        RED = "red"
        BLUE = "blue"

    info = typer.models.OptionInfo()
    result = choice_coercion_annotation(Color, info)
    assert result is not None
    choices, case_sensitive = result
    assert Color.RED in choices
    assert case_sensitive is True
    assert choice_coercion_annotation(str, info) is None


def test_tuple_file_runtime_param(tmp_path: Path) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("first-content\n", encoding="utf-8")
    second.write_text("second-content\n", encoding="utf-8")

    app = typer.Typer()
    seen: list[str] = []

    @app.command()
    def main(files: tuple[typer.FileText, typer.FileText]):
        seen.append(files[0].read())
        seen.append(files[1].read())

    schema = get_command(app).schema
    runtime_param = schema.get_param("files")
    assert isinstance(runtime_param, FileRuntimeParam)
    assert runtime_param.file_annotation is typer.FileText

    result = runner.invoke(app, [str(first), str(second)])
    assert result.exit_code == 0, result.output
    assert seen == ["first-content\n", "second-content\n"]
