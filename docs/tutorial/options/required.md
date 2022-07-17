We said before that *by default*:

* *CLI options* are **optional**
* *CLI arguments* are **required**

Well, that's how they work *by default*, and that's the convention in many CLI programs and systems.

But if you really want, you can change that.

To make a *CLI option* required, pass `...` to `typer.Option()`.

!!! info
    If you hadn't seen that `...` before: it is a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">part of Python and is called "Ellipsis"</a>.

That will tell **Typer** that it's still a *CLI option*, but it doesn't have a default value, and it's required.

Let's make `--lastname` a required *CLI option*:

```Python hl_lines="4"
{!../docs_src/options/required/tutorial001.py!}
```

And test it:

<div class="termy">

```console
// Pass the NAME CLI argument
$ python main.py Camila

// We didn't pass the now required --lastname CLI option
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing option '--lastname'.

// Now update it to pass the required --lastname CLI option
$ python main.py Camila --lastname Gutiérrez

Hello Camila Gutiérrez

// And if you check the help
$ python main.py --help

Usage: main.py [OPTIONS] NAME

Options:
  --lastname TEXT       [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// It now tells you that --lastname is required 🎉
```

</div>
