from typer.testing import CliRunner

from .main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["Camila"], input="camila@example.com\n")
    assert result.exit_code == 0
    assert "Hello Camila, your email is: camila@example.com" in result.output
