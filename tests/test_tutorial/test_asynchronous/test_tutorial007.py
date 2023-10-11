from typer.testing import CliRunner

from docs_src.asynchronous import tutorial007 as mod

app = mod.app

runner = CliRunner()

def test_wait_trio():
    try:
        import trio
        result = runner.invoke(app, ["wait-trio","2"])
        assert result.exit_code == 0
        assert "Waited for 2 seconds using trio (default)" in result.output
    except RuntimeWarning as e:
        assert(str(e) == "You seem to already have a custom sys.excepthook handler installed. I'll skip installing Trio's custom handler, but this means MultiErrors will not show full tracebacks.")


def test_wait_asyncio():
    result = runner.invoke(app, ["wait-asyncio","2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds using asyncio (custom runner)" in result.output