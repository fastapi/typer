from typer.testing import CliRunner

from docs_src.asynchronous import tutorial008 as mod

app = mod.app

runner = CliRunner()


def test_wait_anyio():
    result = runner.invoke(app, ["wait-anyio", "2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds using asyncio via anyio" in result.output


def test_wait_asyncio():
    result = runner.invoke(app, ["wait-asyncio", "2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds using asyncio" in result.output
