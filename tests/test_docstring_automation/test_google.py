import typer
import typer.core
from typer.testing import CliRunner

from . import (
    DOCSTRINGS,
    PARAMS,
    PRIORITY_PARAM_DOC,
    PRIORITY_SUMMARY,
    SUMMARY,
    function_to_test_docstring,
    function_to_test_priority,
)

runner = CliRunner()


def test_google_docstring_parsing():
    app = typer.Typer()
    function_to_test_docstring.__doc__ = DOCSTRINGS["GOOGLE"]
    app.command()(function_to_test_docstring)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Args:" not in result.output
    assert "Returns:" not in result.output
    assert "(str" not in result.output
    assert "(int" not in result.output
    assert "optional" not in result.output
    assert " Defaults to" not in result.output

    assert SUMMARY in result.output
    assert all(param_doc in result.output for param_doc in PARAMS.values())


def test_google_docstring_parsing_priority():
    app = typer.Typer()
    function_to_test_priority.__doc__ = DOCSTRINGS["GOOGLE"]
    app.command(help=PRIORITY_SUMMARY)(function_to_test_priority)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Args:" not in result.output
    assert "Returns:" not in result.output
    assert "(str" not in result.output
    assert "(int" not in result.output
    assert "optional" not in result.output
    assert " Defaults to" not in result.output

    assert SUMMARY not in result.output
    assert PRIORITY_SUMMARY in result.output

    assert PARAMS["param1"] in result.output
    assert PARAMS["param2"] not in result.output
    assert PRIORITY_PARAM_DOC in result.output
    assert PARAMS["param3"] in result.output


# TODO def test_google_docstring_parsing_with line_breaking_param_doc():
