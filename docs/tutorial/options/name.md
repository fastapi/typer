By default **Typer** will create a *CLI option* name from the function parameter.

So, if you have a function with:

```Python
def main(user_name: Optional[str] = None):
    pass
```

or

```Python
def main(user_name: Optional[str] = typer.Option(None)):
    pass
```

**Typer** will create a *CLI option*:

```
--user-name
```

But you can customize it if you want to.

Let's say the function parameter name is `user_name` as above, but you want the *CLI option* to be just `--name`.

You can pass the *CLI option* name that you want to have in the next positional argument passed to `typer.Option()`:

```Python hl_lines="4"
{!../docs_src/options/name/tutorial001.py!}
```

Here you are passing the string `"--name"` as the second positional argument to `typer.Option()`.

!!! info
    "<a href="https://docs.python.org/3.8/glossary.html#term-argument" class="external-link" target="_blank">Positional</a>" means that it's not a function argument with a keyword name.

    For example `show_default=True` is a keyword argument. "`show_default`" is the keyword.

    But in `"--name"` there's no `option_name="--name"` or something similar, it's just the string value `"--name"` that goes in `typer.Option()` after the `...` value passed in the first position.

    That's a "positional argument" in a function.

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice the --name instead of --user-name
Usage: main.py [OPTIONS]

Options:
  --name TEXT           [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Try it
$ python --name Camila

Hello Camila
```

</div>

## *CLI option* short names

A short name is a *CLI option* name with a single dash (`-`) instead of 2 (`--`) and a single letter, like `-n` instead of `--name`.

For example, the `ls` program has a *CLI option* named `--size`, and the same *CLI option* also has a short name `-s`:

<div class="termy">

```console
// With the long name --size
$ ls ./myproject --size

12 first-steps.md   4 intro.md

// With the short name -s
$ ls ./myproject -s

12 first-steps.md   4 intro.md

// Both CLI option names do the same
```

</div>

### *CLI option* short names together

Short names have another feature, when they have a single letter, as in `-s`, you can put several of these *CLI options* together, with a single dash.

For example, the `ls` program has these 2 *CLI options* (among others):

* `--size`: show the sizes of the listed files.
* `--human`: show a human-readable format, like `1MB` instead of just `1024`.

And these 2 *CLI options* have short versions too:

* `--size`: short version `-s`.
* `--human`: short version `-h`.

So, you can put them together with `-sh` or `-hs`:

<div class="termy">

```console
// Call ls with long CLI options
$ ls --size --human

12K first-steps.md   4.0K intro.md

// Now with short versions
$ ls -s -h

12K first-steps.md   4.0K intro.md

// And with short versions together
$ ls -sh

12K first-steps.md   4.0K intro.md

// Order in short versions doesn't matter
$ ls -hs

12K first-steps.md   4.0K intro.md

// They all work the same 🎉
```

</div>

### *CLI option* short names with values

When you use *CLI options* with short names, you can put them together if they are just boolean flags, like `--size` or `--human`.

But if you have a *CLI option* `--file` with a short name `-f` that takes a value, if you put it with other short names for *CLI options*, you have to put it as the last letter, so that it can receive the value that comes right after.

For example, let's say you are decompressing/extracting a file `myproject.tar.gz` with the program `tar`.

You can pass these *CLI option* short names to `tar`:

* `-x`: means "e`X`tract", to decompress and extract the contents.
* `-v`: means "`V`erbose", to print on the screen what it is doing, so you can know that it's decompressing each file and can entertain yourself while you wait.
* `-f`: means "`F`ile", this one requires a value, the compressed file to extract (in our example, this is `myproject.tar.gz`).
    * So if you use all the short names together, this `-f` has to come last, to receive the value that comes next to it.

For example:

<div class="termy">

```console
$ tar -xvf myproject.tar.gz

myproject/
myproject/first-steps.md
myproject/intro.md

// But if you put the -f before
$ tar -fxv myproject.tar.gz

// You get an ugly error
tar: You must specify one of the blah, blah, error, error
```

</div>

### Defining *CLI option* short names

In **Typer** you can also define *CLI option* short names the same way you can customize the long names.

`typer.Option()` receives as a first function argument the default value, e.g. `None`, and all the next *positional* values are to define the *CLI option* name(s).

!!! tip
    Remember the *positional* function arguments are those that don't have a keyword.

    All the other function arguments/parameters you pass to `typer.Option()` like `prompt=True` and `help="This option blah, blah"` require the keyword.

You can overwrite the *CLI option* name to use as in the previous example, but you can also declare extra alternatives, including short names.

For example, extending the previous example, let's add a *CLI option* short name `-n`:

```Python hl_lines="4"
{!../docs_src/options/name/tutorial002.py!}
```

Here we are overwriting the *CLI option* name that by default would be `--user-name`, and we are defining it to be `--name`. And we are also declaring a *CLI option* short name of `-n`.

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// Notice the two CLI option names -n and --name
Usage: main.py [OPTIONS]

Options:
  -n, --name TEXT       [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Try the short version
$ python main.py -n Camila

Hello Camila
```

</div>

### *CLI option* only short name

If you only declare a short name like `-n` then that will be the only *CLI option* name. And neither `--name` nor `--user-name` will be available.

```Python hl_lines="4"
{!../docs_src/options/name/tutorial003.py!}
```

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice there's no --name nor --user-name, only -n
Usage: main.py [OPTIONS]

Options:
  -n TEXT               [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Try it
$ python main.py -n Camila

Hello Camila
```

</div>

### *CLI option* short name and default

Continuing with the example above, as **Typer** allows you to declare a *CLI option* as having only a short name, if you want to have the default long name plus a short name, you have to declare both explicitly:

```Python hl_lines="4"
{!../docs_src/options/name/tutorial004.py!}
```

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice that we have the long version --user-name back
// and we also have the short version -n
Usage: main.py [OPTIONS]

Options:
  -n, --user-name TEXT  [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Try it
$ python main.py --user-name Camila

Hello Camila

// And try the short version
$ python main.py -n Camila
```

</div>

### *CLI option* short names together

You can create multiple short names and use them together.

You don't have to do anything special for it to work (apart from declaring those short versions):

```Python hl_lines="5 6"
{!../docs_src/options/name/tutorial005.py!}
```

!!! tip
    Notice that, again, we are declaring the long and short version of the *CLI option* names.

Check it:

<div class="termy">

```console
$ python main.py --help

// We now have short versions -n and -f
// And also long versions --name and --formal
Usage: main.py [OPTIONS]

Options:
  -n, --name TEXT       [required]
  -f, --formal
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Try the short versions
$ python main.py -n Camila -f

Good day Ms. Camila.

// And try the 2 short versions together
// See how -n has to go last, to be able to get the value
$ python main.py -fn Camila

Good day Ms. Camila.
```

</div>
