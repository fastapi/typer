import typer
from typer.testing import CliRunner

runner = CliRunner()

def test__no_args_is_help__and_no_commands__run_with_no_args__prints_help():
    app = typer.Typer(no_args_is_help=True)
    result = runner.invoke(app, [])
    assert '--help Show this message and exit.' in ' '.join(result.stdout.split())


def test__no_args_is_help__and_one_command__run_with_no_args__prints_help():
    app = typer.Typer(no_args_is_help=True)
    
    @app.command()
    def _():
        ...

    result = runner.invoke(app, [])
    assert '--help Show this message and exit.' in ' '.join(result.stdout.split())


def test__no_args_is_help__and_one_command__run_with_command__executes_command():
    app = typer.Typer(no_args_is_help=True)
    
    @app.command()
    def _():
        print('SUCCESS')

    result = runner.invoke(app, ['-'])
    assert result.stdout == 'SUCCESS\n'
