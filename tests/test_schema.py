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
