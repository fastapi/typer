# Ask with Prompt

When you need to ask the user for info interactively you should normally use [*CLI Option*s with Prompt](options/prompt.md){.internal-link target=_blank}, because they allow using the CLI program in a non-interactive way (for example, a Bash script could use it).

But if you absolutely need to ask for interactive information without using a *CLI option*, you can use `typer.prompt()`:

{* docs_src/prompt/tutorial001_py39.py hl[8] *}

Check it:

<div class="termy">

```console
$ python main.py

# What's your name?:$ Camila

Hello Camila
```

</div>

## Confirm

There's also an alternative to ask for confirmation. Again, if possible, you should use a [*CLI Option* with a confirmation prompt](options/prompt.md){.internal-link target=_blank}:

{* docs_src/prompt/tutorial002_py39.py hl[8] *}

Check it:

<div class="termy">

```console
$ python main.py

# Are you sure you want to delete it? [y/N]:$ y

Deleting it!

// This time cancel it
$ python main.py

# Are you sure you want to delete it? [y/N]:$ n

Not deleting
Aborted!
```

</div>

## Confirm or abort

As it's very common to abort if the user doesn't confirm, there's an integrated parameter `abort` that does it automatically:

{* docs_src/prompt/tutorial003_py39.py hl[8] *}

<div class="termy">

```console
$ python main.py

# Are you sure you want to delete it? [y/N]:$ y

Deleting it!

// This time cancel it
$ python main.py

# Are you sure you want to delete it? [y/N]:$ n

Aborted!
```

</div>

## Prompt with Rich

You can use Rich to prompt the user for input:

{* docs_src/prompt/tutorial004_py39.py hl[2,9] *}

And when you run it, it will look like:

<div class="termy">

```console
$ python main.py

# Enter your name 😎:$ Morty

Hello Morty
```

</div>
