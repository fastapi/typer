from typer.testing import CliRunner

from docs_src.asynchronous import tutorial004 as mod

app = mod.app

runner = CliRunner()

def test_wait():
    result = runner.invoke(app, ["2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds" in result.output