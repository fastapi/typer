import pytest
import typer


def test_invalid_click_type_is_rejected_at_declaration():
    with pytest.raises(TypeError, match="must be a `click.types.ParamType`"):
        typer.Option("x", click_type="int")


def test_valid_click_type_is_kept():
    import click

    option = typer.Option("x", click_type=click.STRING)

    assert option.click_type is click.STRING
