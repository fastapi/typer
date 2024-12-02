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
│   ├── delete.py
```

## Implementation

### Main Application (`main.py`)

```python
import typer
from .users import app as users_app

app = typer.Typer()

app.add_typer(users_app, name="users")

@app.callback()
def callback():
    """
    Awesome CLI application that does everything
    """
    pass

if __name__ == "__main__":
    app()
```

### Users Module (`users/__init__.py`)

```python
import typer

from .add import app as add_app
from .delete import app as delete_app

app = typer.Typer()
app.add_typer(add_app)
app.add_typer(delete_app)
```

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

## Running the Application

To run the application, use the following command:

```bash
$ python mycli/main.py users add John
Adding user: John
```
