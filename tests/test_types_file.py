from io import StringIO
from pathlib import Path

import typer
from typer.testing import CliRunner

app = typer.Typer()


@app.command()
def write(config: typer.FileTextWrite = typer.Option(..., lazy=None)):
    config.write("This is a single line\n")
    print("Config line written")


@app.command()
def write_lazy(config: typer.FileTextWrite = typer.Option(..., lazy=True)):
    config.write("This is a single line\n")
    print("Config line written")


runner = CliRunner()


def test_lazy_file() -> None:
    # dash: written to stdout
    result = runner.invoke(app, ["write", "--config=-"])
    assert result.exit_code == 0
    assert "This is a single line" in result.output
    assert "Config line written" in result.output

    # lazy + file
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["write-lazy", "--config=example.txt"])
        assert result.exit_code == 0
        assert "This is a single line" not in result.output
        assert "Config line written" in result.output
        # test that the file is created
        file_path = Path("example.txt")
        assert file_path.exists()
        with file_path.open("r") as f:
            assert f.read() == "This is a single line\n"

    # lazy + dash: written to stdout (lazy setting is pretty much ignored)
    result = runner.invoke(app, ["write-lazy", "--config=-"])
    assert result.exit_code == 0
    assert "This is a single line" in result.output
    assert "Config line written" in result.output


def test_filelike_conversion() -> None:
    stream = StringIO()
    result = runner.invoke(app, ["write"], default_map={"write": {"config": stream}})
    assert result.exit_code == 0
    assert "Config line written" in result.output
    assert stream.getvalue() == "This is a single line\n"
