import typer
from typer.testing import CliRunner

from docs_src.parameter_types.custom_types import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_parse_custom_type():
    result = runner.invoke(app, ["0", "--custom-opt", "1"])
    assert "custom_arg is <CustomClass: value=000>" in result.output
    assert "custom-opt is <CustomClass: value=111>" in result.output


def test_parse_custom_type_with_default():
    result = runner.invoke(app, ["0"])
    assert "custom_arg is <CustomClass: value=000>" in result.output
    assert "custom-opt is <CustomClass: value=YYY>" in result.output
