#!/usr/bin/env python3

import typer

version_app = typer.Typer()


@version_app.command(help="Print CLI version and exit")
def version():
    print("My CLI Version 1.0")


users_app = typer.Typer(no_args_is_help=True, help="Manage users")


@users_app.command("add", help="Really long help", short_help="Short help")
def add_func(name: str, address: str = None):
    extension = ""
    if address:
        extension = f" at {address}"
    print(f"Adding user: {name}{extension}")


@users_app.command("delete")
def delete_func(name: str):
    print(f"Deleting user: {name}")


@users_app.command("annoy", hidden=True, help="Ill advised annoying someone")
def annoy_user(name: str):
    print(f"Annoying {name}")


user_update_app = typer.Typer(help="Update user info")


@user_update_app.command("name", short_help="change name")
def update_user_name(old: str, new: str):
    print(f"Updating user: {old} => {new}")


@user_update_app.command("address", short_help="change address")
def update_user_addr(name: str, address: str):
    print(f"Updating user {name} address: {address}")


users_app.add_typer(user_update_app, name="update")

pets_app = typer.Typer(no_args_is_help=True)


@pets_app.command("add", short_help="add pet")
def add_pet(name: str):
    print(f"Adding pet named {name}")


@pets_app.command("list")
def list_pets():
    print("Need to compile list of pets")


app = typer.Typer(no_args_is_help=True, command_tree=True, help="Random help")
app.add_typer(version_app)
app.add_typer(users_app, name="users")
app.add_typer(pets_app, name="pets")


if __name__ == "__main__":
    app()
