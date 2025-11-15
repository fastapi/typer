import sys

import pytest
import typer
import typer.completion
from typer.testing import CliRunner
from typing_extensions import Annotated

runner = CliRunner()


def test_rich_utils_click_rewrapp():
    app = typer.Typer(rich_markup_mode="markdown")

    @app.command()
    def main():
        """
        \b
        Some text

        Some unwrapped text
        """
        print("Hello World")

    @app.command()
    def secondary():
        """
        \b
        Secondary text

        Some unwrapped text
        """
        print("Hello Secondary World")

    result = runner.invoke(app, ["--help"])
    assert "Some text" in result.stdout
    assert "Secondary text" in result.stdout
    assert "\b" not in result.stdout
    result = runner.invoke(app, ["main"])
    assert "Hello World" in result.stdout
    result = runner.invoke(app, ["secondary"])
    assert "Hello Secondary World" in result.stdout


def test_rich_help_no_commands():
    """Ensure that the help still works for a Typer instance with no commands, but with a callback."""
    app = typer.Typer(help="My cool Typer app")

    @app.callback(invoke_without_command=True, no_args_is_help=True)
    def main() -> None:
        return None  # pragma: no cover

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Show this message" in result.stdout


def test_rich_doesnt_print_None_default():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(
        name: str,
        option_1: str = typer.Option(
            "option_1_default",
        ),
        option_2: str = typer.Option(
            ...,
        ),
    ):
        print(f"Hello {name}")
        print(f"First: {option_1}")
        print(f"Second: {option_2}")

    result = runner.invoke(app, ["--help"])
    assert "Usage" in result.stdout
    assert "name" in result.stdout
    assert "option-1" in result.stdout
    assert "option-2" in result.stdout
    assert result.stdout.count("[default: None]") == 0
    result = runner.invoke(app, ["Rick", "--option-2=Morty"])
    assert "Hello Rick" in result.stdout
    assert "First: option_1_default" in result.stdout
    assert "Second: Morty" in result.stdout


def test_rich_markup_import_regression():
    # Remove rich.markup if it was imported by other tests
    if "rich" in sys.modules:
        rich_module = sys.modules["rich"]
        if hasattr(rich_module, "markup"):
            delattr(rich_module, "markup")

    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def main(bar: str):
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert "Usage" in result.stdout
    assert "BAR" in result.stdout


# Rich help output formatting tests
# Tests for correct display of 'metavar' in rich help output,
# and includes regression tests for non-rich output and arguments without 'metavar'.


# App with custom metavar for argument
app_with_custom_metavar = typer.Typer()


@app_with_custom_metavar.command()
def greet_with_custom_metavar(
    user: Annotated[str, typer.Argument(metavar="MY_ARG", help="The user to greet.")],
):
    """
    A simple command with an argument using a custom metavar.
    Tests rich help output with explicit argument naming.
    """
    print(f"Hello {user}")


# App with default argument naming (no custom metavar)
app_with_default_argument = typer.Typer()


@app_with_default_argument.command()
def greet_with_default_argument(
    user: Annotated[str, typer.Argument(help="The user to greet.")],
):
    """
    A simple command with an argument using default naming.
    Tests rich help output with parameter-based naming.
    """
    print(f"Hello {user}")


class TestArgumentMetavarDisplay:
    """
    Tests argument metavar display in help output.

    This suite ensures that arguments with custom metavar display
    the metavar as the "Name" and the parameter's type as the "Type".
    It includes tests for rich output and standard Click output,
    covering both custom metavar and default argument naming cases.
    """

    # A single runner instance can be shared
    runner = CliRunner()

    @staticmethod
    def _normalize_output(output: str) -> list[str]:
        """
        Helper function to normalize stdout for reliable assertions.
        It splits output into lines, collapses all internal whitespace to a
        single space, and strips leading/trailing whitespace from each line.
        """
        lines = output.split("\n")
        return [" ".join(line.split()).strip() for line in lines]

    def test_rich_output_with_custom_metavar(self):
        """
        Tests rich help output with custom metavar.

        - With `rich` installed, invokes help on an app with custom metavar.
        - Asserts the "Arguments" panel row correctly shows
          the custom metavar as the name and `TEXT` as the type.
        - Asserts the top-level `Usage:` string also uses the custom metavar.
        """
        # This test requires 'rich' to be installed in the test environment.
        pytest.importorskip("rich")

        # Act
        result = self.runner.invoke(
            app_with_custom_metavar, ["--help"], prog_name="example.py"
        )

        # Assert
        assert result.exit_code == 0
        output = result.stdout
        normalized_lines = self._normalize_output(output)

        # Check Usage string
        assert "Usage: example.py [OPTIONS] MY_ARG" in output

        # Check "Arguments" panel
        # We look for the key elements of the rich table row.
        # Expected row: │ * MY_ARG TEXT [The user to greet.] [required] │
        # We check for a normalized line containing these parts.
        expected_fragment = "MY_ARG TEXT"
        help_fragment = "The user to greet."
        required_fragment = "[required]"

        found = False
        for line in normalized_lines:
            if (
                expected_fragment in line
                and help_fragment in line
                and required_fragment in line
            ):
                found = True
                break

        assert found, (
            f"Could not find correct rich 'Arguments' row.\n"
            f"Expected fragments: '{expected_fragment}', "
            f"'{help_fragment}', '{required_fragment}'\n"
            f"Got output:\n{output}"
        )

    def test_rich_output_with_default_argument_naming(self):
        """
        Tests rich help output with default argument naming.

        - With `rich` installed, invokes help on an app without custom metavar.
        - Asserts the "Arguments" panel falls back to the parameter
          name as the name and `TEXT` as the type.
        - Asserts the `Usage:` string also uses the parameter name.
        """
        pytest.importorskip("rich")

        # Act
        result = self.runner.invoke(
            app_with_default_argument, ["--help"], prog_name="example.py"
        )

        # Assert
        assert result.exit_code == 0
        output = result.stdout
        normalized_lines = self._normalize_output(output)

        # Check Usage string
        assert "Usage: example.py [OPTIONS] USER" in output

        # Check Arguments panel
        # Expected row: │ * user TEXT [The user to greet.] [required] │
        expected_fragment = "user TEXT"
        help_fragment = "The user to greet."
        required_fragment = "[required]"

        found = False
        for line in normalized_lines:
            if (
                expected_fragment in line
                and help_fragment in line
                and required_fragment in line
            ):
                found = True
                break

        assert found, (
            f"Could not find correct rich 'Arguments' fallback row.\n"
            f"Expected fragments: '{expected_fragment}', "
            f"'{help_fragment}', '{required_fragment}'\n"
            f"Got output:\n{output}"
        )

    def test_standard_output_with_custom_metavar(self, monkeypatch):
        """
        Tests standard (non-rich) help output with custom metavar.

        - Simulates `rich` being unavailable by patching `typer.core.HAS_RICH`.
        - Invokes help on an app with custom metavar.
        - Asserts the standard Click help output is generated correctly,
          using the custom metavar in both the `Usage:` string and the `Arguments:` section.
        """
        # Arrange
        # Simulate 'rich' being unavailable.
        # This will cause typer's internal checks to fail and
        # fall back to the standard Click help formatter.
        import typer.core

        monkeypatch.setattr(typer.core, "HAS_RICH", False)

        # Act
        result = self.runner.invoke(
            app_with_custom_metavar, ["--help"], prog_name="example.py"
        )

        # Assert
        assert result.exit_code == 0
        output = result.stdout
        normalized_lines = self._normalize_output(output)

        # Ensure no rich table formatting is present
        assert "│" not in output, "Found rich table characters in non-rich mode"
        assert "━" not in output, "Found rich table characters in non-rich mode"

        # Check Usage string
        assert "Usage: example.py [OPTIONS] MY_ARG" in output

        # Check standard Click "Arguments" section
        # Expected:
        # Arguments:
        #   MY_ARG  The user to greet.  [required]
        expected_fragment = "MY_ARG"
        help_fragment = "The user to greet."
        required_fragment = "[required]"

        found = False
        in_arguments_section = False
        for line in normalized_lines:
            if line.startswith("Arguments:"):
                in_arguments_section = True
                continue

            if in_arguments_section:
                # Check for the argument line
                if (
                    expected_fragment in line
                    and help_fragment in line
                    and required_fragment in line
                ):
                    found = True
                    break
                # Stop if we hit another section
                if line.startswith("Options:"):
                    break

        assert found, (
            f"Could not find standard 'Arguments' line.\n"
            f"Expected fragments: '{expected_fragment}', "
            f"'{help_fragment}', '{required_fragment}'\n"
            f"Got output:\n{output}"
        )
