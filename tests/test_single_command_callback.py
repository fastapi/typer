import typer
from typer.testing import CliRunner

runner: CliRunner = CliRunner()


def test_result_callback_single_command() -> None:
    # A list to capture the result from the callback
    captured_results: list[str] = []

    def my_callback(value: str) -> None:
        captured_results.append(value)

    # Create app with a result_callback
    app: typer.Typer = typer.Typer(result_callback=my_callback)

    @app.command()
    def main() -> str:
        return "single_command_result"

    # Invoke the app (using the single command fast-path)
    result = runner.invoke(app, [])

    # Verify the command ran successfully
    assert result.exit_code == 0

    # CRITICAL: Verify the callback was actually executed
    assert "single_command_result" in captured_results, (
        "Result callback was not triggered for single command!"
    )


def test_result_callback_single_command_placeholder() -> None:
    from typer.models import DefaultPlaceholder

    # A list to capture the result from the callback
    captured_results: list[str] = []

    def my_callback(value: str) -> None:
        captured_results.append(value)

    # Create app and manually inject a DefaultPlaceholder for the result_callback
    app = typer.Typer()
    app.info.result_callback = DefaultPlaceholder(my_callback)

    @app.command()
    def main() -> str:
        return "placeholder_result"

    # Invoke the app
    result = runner.invoke(app, [])

    # Verify the command ran successfully
    assert result.exit_code == 0

    # Verify the callback was actually executed via the placeholder path
    assert "placeholder_result" in captured_results, (
        "Result callback was not triggered via placeholder!"
    )
