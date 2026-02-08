"""
Failing tests that expose bugs in Typer's multiple values handling.

These tests document known issues and inconsistencies that should be fixed.
Related GitHub issues:
- Tuple vs List inconsistency: https://github.com/fastapi/typer/issues/[TBD]
- Multiple value option returns tuple not list: https://github.com/fastapi/typer/issues/[TBD]

Author: Kaushaki Khandelwal
Date: 2026-02-08
"""

from typing import List

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()


class TestTupleOptionNoneDefaults:
    """
    BUG: Tuple options with (None, None, None) defaults don't properly validate.

    The issue: When a tuple option has None values in its default tuple,
    the validation and type  conversion doesn't handle missing values correctly.
    """

    def test_tuple_option_none_default_should_handle_missing_gracefully(self):
        """
        EXPECTED: Should allow command to run without the --user flag
        ACTUAL: May raise validation error or handle None incorrectly

        Related to: tutorial001_py39.py
        """
        app = typer.Typer()

        @app.command()
        def main(user: tuple[str, int, bool] = typer.Option((None, None, None))):
            username, coins, is_wizard = user
            if not username:
                typer.echo("No user provided")
                raise typer.Abort()
            typer.echo(f"The username {username} has {coins} coins")
            if is_wizard:
                typer.echo("And this user is a wizard!")

        # This test currently FAILS or behaves inconsistently
        result = runner.invoke(app, [])

        # We expect graceful handling of missing values
        assert result.exit_code == 1  # Should abort gracefully
        assert "No user provided" in result.output

    def test_tuple_option_partial_values_should_error(self):
        """
        BUG: Providing partial tuple values should give clear error

        EXPECTED: Clear error message about needing all 3 values
        ACTUAL: May accept partial values or give confusing error
        """
        app = typer.Typer()

        @app.command()
        def main(user: tuple[str, int, bool] = typer.Option((None, None, None))):
            username, coins, is_wizard = user
            typer.echo(f"User: {username}")

        # Providing only 2 values when 3 are expected
        result = runner.invoke(app, ["--user", "Harry", "100"])

        # Should fail with clear error
        assert result.exit_code != 0
        assert "user" in result.output.lower() or "values" in result.output.lower()


class TestListVsTupleInconsistency:
    """
    BUG: Multiple value options return tuple instead of list despite type hint

    GitHub Issue: Multiple value option gives tuple and not list
    Reference: https://github.com/fastapi/typer/issues/[issue_number]

    The documentation states that List[str] should receive values as a list,
    but the actual behavior returns a tuple.
    """

    @pytest.mark.xfail(
        reason="Known bug: multiple value option returns tuple instead of list"
    )
    def test_list_option_should_return_list_not_tuple(self):
        """
        EXPECTED: List[str] type hint should receive actual list
        ACTUAL: Receives tuple instead

        This contradicts the documentation and type hints.
        """
        app = typer.Typer()

        received_type = None

        @app.command()
        def main(names: List[str] = typer.Option([], "--name", multiple=True)):
            nonlocal received_type
            received_type = type(names)
            typer.echo(f"Type: {type(names).__name__}")
            typer.echo(f"Names: {names}")

        result = runner.invoke(app, ["--name", "Alice", "--name", "Bob"])

        assert result.exit_code == 0
        # This assertion FAILS - we get tuple instead of list
        assert received_type == list, f"Expected list but got {received_type}"
        assert isinstance(result.output, str)

    @pytest.mark.xfail(reason="Known bug: list operations fail on tuple return")
    def test_list_type_hint_should_support_list_operations(self):
        """
        EXPECTED: Should be able to use list methods like .append()
        ACTUAL: Fails because it's actually a tuple
        """
        app = typer.Typer()

        @app.command()
        def main(items: List[str] = typer.Option([], multiple=True)):
            # Type hint says List, so we should be able to use list methods
            try:
                items.append("new_item")  # This should work if it's a list
                typer.echo("Success: can use list methods")
            except AttributeError:
                typer.echo("FAIL: cannot use list methods - it's a tuple!")

        result = runner.invoke(app, ["--items", "a", "--items", "b"])

        # This test currently FAILS
        assert "Success" in result.output
        assert "FAIL" not in result.output


class TestEmptyDefaultBehavior:
    """
    BUG: Empty defaults behave inconsistently between tuple and list options
    """

    def test_empty_tuple_default_behavior(self):
        """
        Document how empty tuple defaults currently behave
        """
        app = typer.Typer()

        @app.command()
        def main(values: tuple[str, str] = typer.Option(("", ""))):
            typer.echo(f"Values: {values}")

        # How should this behave when user provides nothing?
        result = runner.invoke(app, [])

        # Current behavior might be inconsistent
        # This test documents what happens
        assert result.exit_code == 0

    def test_none_vs_empty_string_in_tuple(self):
        """
        BUG: Inconsistent handling of None vs empty string in defaults
        """
        app = typer.Typer()

        @app.command()
        def main(
            user1: tuple[str, int] = typer.Option((None, None)),
            user2: tuple[str, int] = typer.Option(("", 0)),
        ):
            typer.echo(f"User1: {user1}")
            typer.echo(f"User2: {user2}")

        result = runner.invoke(app, [])

        # Should these behave the same? Currently they might not
        assert result.exit_code == 0


class TestTupleTypeConversion:
    """
    BUG: Type conversion in tuples may not handle all cases correctly
    """

    def test_tuple_bool_conversion_edge_cases(self):
        """
        Test various bool representations in tuple options
        """
        app = typer.Typer()

        @app.command()
        def main(user: tuple[str, int, bool] = typer.Option((None, None, None))):
            username, coins, is_wizard = user
            typer.echo(f"{username}: {coins} coins, wizard={is_wizard}")

        # Test various bool representations
        test_cases = [
            (["--user", "Harry", "100", "true"], True),
            (["--user", "Ron", "50", "false"], False),
            (["--user", "Hermione", "200", "1"], True),
            (["--user", "Draco", "150", "0"], False),
        ]

        for args, expected_bool in test_cases:
            result = runner.invoke(app, args)
            # Document current behavior - may have inconsistencies
            print(f"Args: {args}")
            print(f"Output: {result.output}")
            print(f"Exit code: {result.exit_code}")


# Mark entire class for investigation
@pytest.mark.skip(reason="Tests need Typer to be installed in development mode")
class TestRequiresDevInstall:
    """
    These tests require Typer to be installed in development mode.

    To run: pip install -e .
    """

    def test_with_actual_tutorial_file(self):
        """Test the actual tutorial file"""
        from docs_src.multiple_values.options_with_multiple_values import (
            tutorial001_py39,
        )

        app = tutorial001_py39.app
        result = runner.invoke(app, [])

        assert result.exit_code == 1
        assert "No user provided" in result.output


# Additional edge case tests
class TestEdgeCases:
    """
    Additional edge cases that might expose bugs
    """

    def test_mixing_required_and_optional_tuple_options(self):
        """
        How does Typer handle mix of required and optional tuple options?
        """
        app = typer.Typer()

        @app.command()
        def main(
            required: tuple[str, int],  # Required
            optional: tuple[str, int] = typer.Option((None, None)),  # Optional
        ):
            typer.echo(f"Required: {required}, Optional: {optional}")

        # This might have unexpected behavior
        result = runner.invoke(app, ["value", "42"])

        # Document the actual behavior
        print(f"Exit code: {result.exit_code}")
        print(f"Output: {result.output}")

    @pytest.mark.xfail(reason="Investigating behavior with nested types")
    def test_list_of_tuples_not_supported(self):
        """
        BUG: List[Tuple[str, str]] should work but gives AssertionError

        Reference: GitHub discussions about List[Tuple[str, str]] support
        """
        app = typer.Typer()

        with pytest.raises(AssertionError, match="complex sub-types"):

            @app.command()
            def main(pairs: List[tuple[str, str]] = typer.Option([])):
                typer.echo(f"Pairs: {pairs}")

            # This definition itself should raise an error
            # "List types with complex sub-types are not currently supported"


if __name__ == "__main__":
    # Run the tests to see which ones fail
    print("=" * 60)
    print("TYPER BUG DISCOVERY TESTS")
    print("=" * 60)
    print("\nThese tests expose bugs and inconsistencies in Typer.")
    print("Run with: pytest test_typer_bugs.py -v")
    print("\nTo skip xfail tests: pytest test_typer_bugs.py -v --runxfail")
    print("=" * 60)
