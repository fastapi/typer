# Install **Typer**

The first step is to set up your project and add **Typer**.

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then create a project and add Typer:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add typer
---> 100%
```

</div>

`uv add` creates the project's virtual environment in `.venv`, adds Typer to `pyproject.toml`, and creates `uv.lock` so the same package versions can be installed later.

/// details | What these commands do

* `uv init`: create a new Python project.
* `awesome-project`: create the project in a new directory with this name.
* `--bare`: create only the minimal `pyproject.toml` file, without generating a sample `main.py`, `README.md`, or other files. You will create the application files yourself in the next steps of this tutorial.

Then `cd awesome-project` enters the new project directory before adding Typer.

`uv` will use a compatible Python version already installed on your system, or download one if needed.

When you run `uv add`, it selects compatible versions of Typer and all the packages Typer depends on. It records the exact versions in `uv.lock`, making it possible to install the same package versions later on another computer or when distributing the application.

Creating or updating this file is called [**locking** the project dependencies](https://docs.astral.sh/uv/concepts/projects/sync/). `uv` does this automatically when you add a package.

///

By default, `typer` comes with `rich` and `shellingham`.

## Activate the Virtual Environment

`uv add typer` installs both the Typer library and the `typer` command in the project's `.venv`.

You can normally run project commands with `uv run`. But to configure and use shell completion for the first-class `typer` command, activate the project's virtual environment so that `typer` is available directly in your shell.

//// tab | Linux, macOS

<div class="termy">

```console
$ source .venv/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .venv\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

<div class="termy">

```console
$ source .venv/Scripts/activate
```

</div>

////

Enable completion for your current shell with:

<div class="termy">

```console
$ typer --install-completion
```

</div>

Restart your terminal for the new completion configuration to take effect.

Activate the project's virtual environment again in each new terminal session where you want to use the `typer` command directly.

/// details | Using `pip` instead

If you prefer to manage a virtual environment and packages manually, create and activate a virtual environment and then install Typer with `pip install typer`.

Read the [Virtual Environments guide](https://tiangolo.com/guides/virtual-environments/) for the detailed steps.

///

## AI Agent Skills

Typer includes an official skill for AI coding agents. It is bundled with the package, so its guidance stays aligned with the version of Typer installed in your project and updates when you update Typer.

After installing Typer in your project, you can install the skill with <a href="https://library-skills.io">Library Skills</a>:

```bash
uvx library-skills
```

/// note

`uvx` is an alias for `uv tool run`. It runs Library Skills in a temporary, isolated environment while Library Skills scans the packages installed in your project.

///

The skill is compatible with Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode, and most other coding agents. For Claude Code, select `.claude/skills` when asked where to install the skill.
