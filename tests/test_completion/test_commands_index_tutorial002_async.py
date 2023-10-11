from typer.testing import CliRunner

from tests.test_completion.for_testing import (
    commands_index_tutorial002_async as async_mod,
)

app = async_mod.app

runner = CliRunner()


def test_create():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating user: Hiro Hamada" in result.output


def test_delete():
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Deleting user: Hiro Hamada" in result.output
