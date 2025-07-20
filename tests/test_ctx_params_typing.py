"""
Test for improved type hints in Context.command.params

This test verifies that the Context class now has proper type hints
for the command.params attribute, allowing IDE autocompletion and
type checking tools like mypy to work correctly.
"""

from typing import List

import click
import typer
from typer.models import Context


def test_context_command_params_typing():
    """Test that Context.command.params is properly typed as List[click.Parameter]."""

    def sample_callback(ctx: Context, name: str = typer.Argument(...)) -> None:
        """Sample callback function that uses Context."""
        # This should be properly typed now
        params: List[click.Parameter] = ctx.command.params

        # Test that we can access Parameter attributes with proper typing
        for param in params:
            # These should all be properly typed and autocompleted by IDEs
            param_name: str = param.name
            param_type: click.ParamType = param.type
            param_help: str = param.help or ""
            param_required: bool = param.required

            # Verify the param is indeed a click.Parameter
            assert isinstance(param, click.Parameter)
            assert hasattr(param, "name")
            assert hasattr(param, "type")

    # Create a Typer app to test with
    app = typer.Typer()
    app.command()(sample_callback)

    # Convert to click command and create context
    click_command = typer.main.get_command(app)
    ctx = Context(click_command)

    # Verify the command has params
    assert hasattr(ctx.command, "params")
    assert isinstance(ctx.command.params, list)

    # If there are params, they should be click.Parameter instances
    for param in ctx.command.params:
        assert isinstance(param, click.Parameter)


def test_context_typing_with_options_and_arguments():
    """Test Context typing works with both Options and Arguments."""

    def cmd_with_params(
        ctx: Context,
        name: str = typer.Argument(..., help="The name argument"),
        count: int = typer.Option(1, help="The count option"),
        verbose: bool = typer.Option(False, "--verbose", help="Verbose output"),
    ) -> None:
        """Command with both arguments and options."""
        # Access command params with proper typing
        params: List[click.Parameter] = ctx.command.params

        # Should have 3 params: name (argument), count (option), verbose (option)
        # Plus potentially help option
        assert len(params) >= 3

        # Check that params have expected attributes
        for param in params:
            assert hasattr(param, "name")
            assert isinstance(param.name, str)
            assert hasattr(param, "help")

            # Test type hints work for common parameter operations
            if param.name == "name":
                assert isinstance(param, click.Argument)
            elif param.name in ["count", "verbose"]:
                assert isinstance(param, click.Option)

    # Create app and get click command
    app = typer.Typer()
    app.command()(cmd_with_params)
    click_command = typer.main.get_command(app)

    # Create context - this should work with our improved typing
    ctx = Context(click_command)

    # Verify we can access params with proper typing
    assert isinstance(ctx.command.params, list)
    assert all(isinstance(p, click.Parameter) for p in ctx.command.params)


def test_context_inheritance_from_click():
    """Test that our Context still properly inherits from click.Context."""

    # Create a basic command
    click_command = click.Command("test")

    # Our Context should work with regular click commands too
    ctx = Context(click_command)

    # Should still be a click.Context
    assert isinstance(ctx, click.Context)
    assert isinstance(ctx, Context)

    # Should have properly typed command
    assert hasattr(ctx, "command")
    assert hasattr(ctx.command, "params")
    assert isinstance(ctx.command.params, list)


def sample_function_for_mypy_verification(ctx: Context) -> None:
    """
    This function demonstrates the improved typing for static analysis.

    When this file is checked with mypy, it should not produce any type errors
    and should properly infer the types of param attributes.
    """
    # These assignments should all type-check correctly with mypy
    params: List[click.Parameter] = ctx.command.params

    for param in params:
        # mypy should now know these are properly typed
        name: str = param.name
        help_text: str = param.help or ""
        required: bool = param.required

        # mypy should also allow method calls on Parameter
        param_decl: List[str] = param.opts
        full_process_value = param.full_process_value

        # Type annotations should work for isinstance checks
        if isinstance(param, click.Option):
            # mypy should know this is an Option-specific attribute
            show_default: bool = param.show_default
        elif isinstance(param, click.Argument):
            # mypy should know this is an Argument
            assert param.nargs != 0
