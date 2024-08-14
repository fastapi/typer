# Ask with Prompt

When you need to ask the user for info interactively you should normally use [*CLI Option*s with Prompt](options/prompt.md){.internal-link target=_blank}, because they allow using the CLI program in a non-interactive way (for example, a Bash script could use it).

But if you absolutely need to ask for interactive information without using a *CLI option*, you can use `typer.prompt()`:

```Python hl_lines="5"
{!../docs_src/prompt/tutorial001.py!}
```

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

```Python hl_lines="5"
{!../docs_src/prompt/tutorial002.py!}
```

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

```Python hl_lines="5"
{!../docs_src/prompt/tutorial003.py!}
```

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

If you installed Rich as described in [Printing and Colors](printing.md){.internal-link target=_blank}, you can use Rich to prompt the user for input:

```Python hl_lines="2  6"
{!../docs_src/prompt/tutorial004.py!}
```

And when you run it, it will look like:

<div class="termy">

```console
$ python main.py

# Enter your name 😎:$ Morty

Hello Morty
```

</div>
