# Multi-File Applications

When your CLI application grows, you can split it into multiple files and modules. This pattern helps maintain clean and organized code structure.

This tutorial will show you how to use `add_typer` to create sub commands and organize your commands in multiple files.

We will create a simple CLI with the following commands:

- `version`
- `users add NAME`
- `users delete NAME`

## CLI structure

Here is the structure we'll be working with:

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

`mycli` will be our package, and it will contain the following modules:

- `main.py`: The main module that will import the `version` and `users` modules.
- `version.py`: A module that will contain the `version` command.
- `users/`: A package that will contain the `add` and `delete` commands.

## Implementation

Let's start implementing our CLI! We'll create the `version` module, the `main` module, and the `users` package.

### Version Module (`version.py`)

Let's start by creating the `version` module. This module will contain the `version` command.

{* docs_src/splitting_apps/version.py *}

In this file we are creating a new Typer app instance for the version command. This is not required in single-file applications, but in the case of multi-file applications it will allow us to include this command in the main application using `add_typer`.

Let's see that next!

### Main Module (`main.py`)

The main module will be the entry point of the application. It will import the version module and the users module. We'll see how to implement the user module in the next section.

{* docs_src/splitting_apps/main.py hl[8,9] *}

In this module, we import the `version` and `users` modules and add them to the main app using `add_typer`. For the `users` module, we specify the name as `users` to group the commands under the `users` namespace.

Let's now create the `users` module with the `add` and `delete` commands.

### Users Add Command (`users/add.py`)

{* docs_src/splitting_apps/users/add.py *}

Like the `version` module, we create a new Typer app instance for the `users/add` command. This allows us to include the `add` command in the users app.

### Users Delete Command (`users/delete.py`)

{* docs_src/splitting_apps/users/delete.py *}

And once again, we create a new Typer app instance for the `users/delete` command. This allows us to include the `delete` command in the users app.

### Users' app (`users/__init__.py`)

Finally, we need to create an `__init__.py` file in the `users` directory to define the `users` app.

{* docs_src/splitting_apps/users/__init__.py *}

Similarly to the `version` module, we create a new `Typer` app instance for the `users` module. This allows us to include the `add` and `delete` commands in the users app.

## Running the Application

Now we are ready to run the application!

To run the application, execute the `main.py` file:

<div class="termy">

```console
$ python main.py version

My CLI Version 1.0

$ python main.py users add Camila

Adding user: Camila
```

</div>
