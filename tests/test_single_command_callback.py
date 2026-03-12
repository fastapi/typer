import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_result_callback_single_command():
    # A list to capture the result from the callback
    captured_results: list[str] = []

    def my_callback(value: str) -> None:
        captured_results.append(value)

    # Create app with a result_callback
    app = typer.Typer(result_callback=my_callback)

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
