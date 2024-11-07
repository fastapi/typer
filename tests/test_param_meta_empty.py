import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_default_with_class_with_custom_eq():
    app = typer.Typer()

    from typer.models import ParamMeta

    class StupidClass:
        def __init__(self, a):
            self.a = a

        def __eq__(self, other) -> bool:
            if other is ParamMeta.empty:
                return True
            try:
                return self.a == other.a
            except Exception:
                return False

        def __ne__(self, other: object) -> bool:
            return not self.__eq__(other)

    @app.command()
    def cmd(val=StupidClass(42)):
        print(val)

    assert StupidClass(666) == ParamMeta.empty
    assert StupidClass(666) != StupidClass(1)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert "StupidClass" in result.output
