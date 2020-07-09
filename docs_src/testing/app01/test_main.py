from typer.testing import CliRunner

from .main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["Camila", "--city", "Berlin"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.stdout
    assert "Let's have a coffee in Berlin" in result.stdout
