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

{* docs_src/splitting_apps/version.py hl[3,6,7,8] *}

In this file we are creating a new Typer app instance for the version command. This is not required in single-file applications, but in the case of multi-file applications it will allow us to include this command in the main application using `add_typer`.

### Main Module (`main.py`)

The main module will be the entry point of the application. It will import the version module and the users module. We'll see how to implement the user module in the next section.

{* docs_src/splitting_apps/main.py hl[8,9] *}

In this module, we import the `version` and `users` modules and add them to the main app using `add_typer`. For the `users` module, we specify the name as `users` to group the commands under the `users` namespace.

Let's now create the `users` module with the `add` and `delete` commands.

### Users Add Command (`users/add.py`)

{* docs_src/splitting_apps/users/add.py *}

### Users Delete Command (`users/delete.py`)

{* docs_src/splitting_apps/users/delete.py *}

### Users' app

{* docs_src/splitting_apps/users/__init__.py *}

Similar to the `version` module, we create a new `Typer` app instance for the `users` module. This allows us to include the `add` and `delete` commands in the users app.
