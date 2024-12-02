# Typer Multi-File Applications

When your CLI application grows, you can split it into multiple files and modules. This pattern helps maintain clean and organized code structure.

In this tutorial, you will learn how to create a multi-file Typer application.

## Basic Structure

Here is a basic structure for a multi-file Typer application:

```text
mycli/
├── __init__.py
├── main.py
├── users/
│   ├── __init__.py
│   ├── add.py
│   └── delete.py
└── version.py
```

This application will have the following commands:

- `users add`
- `users delete`
- `version`

## Implementation

### Version Module (`version.py`)

Let's start by creating a simple module that prints the version of the application.

```python
import typer

app = typer.Typer()

@app.command()
def version():
    typer.echo("MyCLI version 1.0.0")
```

In this example, we are creating a new `Typer` app instance for the `version` module. This is not required for a single-file application but is necessary for a multi-file application, as it will allow us to include this command in the main app using `add_typer`.

### Main Module (`main.py`)

The main module will be the entry point of the application. It will import the version module and the users module.

```python
import typer

from version import app as version_app
from users import app as users_app

app = typer.Typer()

app.add_typer(version_app)
app.add_typer(users_app, name="users")
```

In this module, we import the `version` and `users` modules and add them to the main app using `add_typer`. For the `users` module, we specify the name as `users` to group the commands under the `users` namespace.

Let's now create the `users` module with the `add` and `delete` commands.

### Users Add Command (`users/add.py`)

```python
import typer

app = typer.Typer()

@app.command()
def add(name: str):
    typer.echo(f"Adding user: {name}")
```

### Users Delete Command (`users/delete.py`)

```python
import typer

app = typer.Typer()

@app.command()
def delete(name: str):
    typer.echo(f"Deleting user: {name
```

Similar to the `version` module, we create a new `Typer` app instance for the `users` module. This allows us to include the `add` and `delete` commands in the users app.
