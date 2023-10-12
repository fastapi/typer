from typer.testing import CliRunner

from docs_src.asynchronous import tutorial007 as mod

app = mod.app

runner = CliRunner()


def test_wait_trio():
    result = runner.invoke(app, ["wait-trio", "2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds using trio (default)" in result.output


def test_wait_asyncio():
    result = runner.invoke(app, ["wait-asyncio", "2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds using asyncio (custom runner)" in result.output
