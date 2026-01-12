from typer.testing import CliRunner

from docs_src.commands.index import tutorial005_py39 as mod

app = mod.app
runner = CliRunner()


def test_creates_successfully():
    """Verify the example runs without errors"""
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating..." in result.output

    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Deleting..." in result.output


def test_shows_suggestion():
    """Verify command suggestions appear for typos"""
    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "Did you mean 'create'?" in result.output
