"""Tests defining the contract for automatic Typer command discovery."""

from __future__ import annotations

import importlib

import click
import pytest
import typer
from typer.discovery import TyperDiscoveryError, register_package
from typer.main import get_command
from typer.testing import CliRunner

runner = CliRunner()

TARGET_PACKAGE = "tests.assets.discovery_targets"
FAILING_PACKAGE = "tests.assets.discovery_package"
FAILING_MODULE = f"{FAILING_PACKAGE}.failing"


def invoke(app: typer.Typer, *args: str) -> str:
    result = runner.invoke(app, list(args))
    assert result.exit_code == 0, result.output
    return result.output


def command_names(app: typer.Typer) -> list[str]:
    click_command = get_command(app)
    ctx = click.Context(click_command)
    return click_command.list_commands(ctx)


def test_register_package_discovers_modules() -> None:
    app = typer.Typer()
    package = importlib.import_module(TARGET_PACKAGE)

    register_package(app, package)

    output = invoke(app, "users", "create", "Ada")
    assert "created user Ada" in output

    nested = invoke(app, "inventory", "summary")
    assert "inventory summary" in nested

    audit = invoke(app, "inventory", "audit", "run", "3")
    assert "inventory audit level 3" in audit


def test_register_package_namespace_prefix() -> None:
    app = typer.Typer()
    package = importlib.import_module(TARGET_PACKAGE)

    register_package(app, package, namespace="ops")

    namespaced = invoke(app, "ops", "users", "deactivate", "Neo")
    assert "deactivated user Neo" in namespaced


def test_register_package_filters_scope() -> None:
    app = typer.Typer()
    package = importlib.import_module(TARGET_PACKAGE)

    register_package(app, package, filters=["inventory.*"])

    invoke(app, "inventory", "audit", "run")

    missing = runner.invoke(app, ["users", "create", "Eve"])
    assert missing.exit_code != 0
    assert "No such command 'users'" in missing.output


def test_register_package_surfaces_import_failures_with_module_name() -> None:
    app = typer.Typer()
    package = importlib.import_module(FAILING_PACKAGE)

    with pytest.raises(TyperDiscoveryError) as excinfo:
        register_package(app, package)

    message = str(excinfo.value)
    assert message == f"Failed to import module '{FAILING_MODULE}'"


def test_register_package_is_idempotent() -> None:
    app = typer.Typer()
    package = importlib.import_module(TARGET_PACKAGE)

    register_package(app, package)
    register_package(app, package)

    names = command_names(app)
    assert names.count("users") == 1
    assert names.count("inventory") == 1

    output = invoke(app, "users", "create", "Ada")
    assert "created user Ada" in output


def test_register_package_preserves_manual_commands() -> None:
    app = typer.Typer()

    @app.command()
    def manual(name: str) -> None:
        typer.echo(f"manual {name}")

    package = importlib.import_module(TARGET_PACKAGE)

    register_package(app, package, namespace="ops")

    manual_output = invoke(app, "manual", "Casey")
    assert "manual Casey" in manual_output

    namespaced = invoke(app, "ops", "users", "create", "Zoe")
    assert "created user Zoe" in namespaced


def test_register_package_handles_name_collisions() -> None:
    app = typer.Typer()

    @app.command()
    def users() -> None:
        typer.echo("manual users command")

    package = importlib.import_module(TARGET_PACKAGE)

    with pytest.raises(TyperDiscoveryError):
        register_package(app, package)

    register_package(app, package, namespace="pkg")

    manual_output = invoke(app, "users")
    assert "manual users command" in manual_output

    namespaced = invoke(app, "pkg", "users", "create", "Ana")
    assert "created user Ana" in namespaced


def test_register_package_filters_can_skip_failing_modules() -> None:
    package = importlib.import_module(FAILING_PACKAGE)

    unfiltered_app = typer.Typer()
    with pytest.raises(TyperDiscoveryError) as excinfo:
        register_package(unfiltered_app, package)

    assert str(excinfo.value) == f"Failed to import module '{FAILING_MODULE}'"

    filtered_app = typer.Typer()
    register_package(filtered_app, package, filters=["users", "inventory.*"])

    invoke(filtered_app, "users", "create", "Rory")
    summary = invoke(filtered_app, "inventory", "summary")
    assert "inventory summary" in summary

    audit = invoke(filtered_app, "inventory", "audit", "run", "4")
    assert "inventory audit level 4" in audit
