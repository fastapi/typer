from pathlib import Path

import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_coercion() -> None:
    app = typer.Typer()
    seen: dict[str, object] = {}

    @app.command()
    def main(items: list[int], active: bool = False, val=42):
        seen["items"] = items
        seen["active"] = active
        seen["val"] = val

    result = runner.invoke(app, ["1", "2", "--active", "--val", "7"])
    assert result.exit_code == 0, result.output
    assert seen == {"items": [1, 2], "active": True, "val": 7}


def test_coercion_invalid() -> None:
    app = typer.Typer()

    @app.command()
    def main(age: int):
        pass

    result = runner.invoke(app, ["not-an-int"])
    assert "Input should be a valid integer" in result.stderr
    assert result.exit_code == 2


def test_coercion_path(tmp_path: Path) -> None:
    target = tmp_path / "config.txt"
    target.write_text("hello\n", encoding="utf-8")
    app = typer.Typer()
    seen: list[Path] = []

    @app.command()
    def main(config: Path = typer.Option(..., exists=True)):
        seen.append(config)

    result = runner.invoke(app, ["--config", str(target)])
    assert result.exit_code == 0
    assert seen == [target]


def test_coercion_tuple_files(tmp_path: Path) -> None:
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

    result = runner.invoke(app, [str(first), str(second)])
    assert result.exit_code == 0, result.output
    assert seen == ["first-content\n", "second-content\n"]


def test_passthrough_runtime_param_default() -> None:
    class Widget:
        def __init__(self, value: int) -> None:
            self.value = value

        def __repr__(self) -> str:
            return f"Widget({self.value})"

    app = typer.Typer()
    seen: dict[str, Widget] = {}

    @app.command()
    def main(val=Widget(42)):
        seen["val"] = val

    param = next(p for p in typer.main.get_command(app).params if p.name == "val")
    assert param.runtime_param is not None
    assert param.runtime_param.annotation is Widget

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert isinstance(seen["val"], Widget)
    assert seen["val"].value == 42

    result = runner.invoke(app, ["--val", "666"])
    assert result.exit_code == 2
    # This doesn't work because there's no parser
    assert "is not a valid Widget" in result.output


def test_widget_parsed_from_cli_with_parser() -> None:
    class Widget:
        def __init__(self, value: int) -> None:
            self.value = value

        def __repr__(self) -> str:
            return f"Widget({self.value})"

    def parse_widget(value: str) -> Widget:
        return Widget(int(value))

    app = typer.Typer()
    seen: dict[str, Widget] = {}

    @app.command()
    def main(val: Widget = typer.Option("42", parser=parse_widget)):
        seen["val"] = val

    param = next(p for p in typer.main.get_command(app).params if p.name == "val")
    assert param.runtime_param is not None
    assert param.runtime_param.annotation is Widget

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert isinstance(seen["val"], Widget)
    assert seen["val"].value == 42

    result = runner.invoke(app, ["--val", "666"])
    assert result.exit_code == 0
    assert isinstance(seen["val"], Widget)
    assert seen["val"].value == 666
