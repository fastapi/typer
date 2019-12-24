from click.testing import Result, CliRunner as ClickCliRunner  # noqa
from typer.main import get_command as _get_command


class CliRunner(ClickCliRunner):
    def invoke(
        self,
        cli,
        args=None,
        input=None,
        env=None,
        catch_exceptions=True,
        color=False,
        mix_stderr=False,
        **extra
    ) -> Result:
        use_cli = _get_command(cli)
        return super().invoke(
            use_cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            color=color,
            mix_stderr=mix_stderr,
            **extra
        )
