# Typer App

## Explicit application

So far, you have seen how to create a single function and then pass that function to `typer.run()`.

For example:

{* docs_src/first_steps/tutorial002.py hl[9] *}

But that is actually a shortcut. Under the hood, **Typer** converts that to a CLI application with `typer.Typer()` and executes it. All that inside of `typer.run()`.

There's also a more explicit way to achieve the same:

{* docs_src/typer_app/tutorial001.py hl[3,6,12] *}

When you use `typer.run()`, **Typer** is doing more or less the same as above, it will:

* Create a new `typer.Typer()` "application".
* Create a new "`command`" with your function.
* Call the same "application" as if it was a function with "`app()`".

/// info | `@decorator` Info

That `@something` syntax in Python is called a "decorator".

You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

A "decorator" takes the function below and does something with it.

In our case, this decorator tells **Typer** that the function below is a "`command`".
You will learn more about commands later in the section [commands](./commands/index.md){.internal-link target=_blank}.

///

Both ways, with `typer.run()` and creating the explicit application, achieve almost the same.

/// tip

If your use case is solved with just `typer.run()`, that's fine, you don't have to create the explicit `app` and use `@app.command()`, etc.

You might want to do that later when your app needs extra features, but if it doesn't need them yet, that's fine.

///

If you run the second example, with the explicit `app`, it works exactly the same:

<div class="termy">

```console
// Without a CLI argument
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.

// With the NAME CLI argument
$ python main.py Camila

Hello Camila

// Asking for help
$ python main.py  --help

Usage: main.py [OPTIONS] NAME

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## CLI application completion

There's a little detail that is worth noting here.

Now the help shows two new *CLI options*:

* `--install-completion`
* `--show-completion`

To get shell/tab completion, it's necessary to build a package that you and your users can install and **call directly**.

So instead of running a Python script like:

<div class="termy">

```console
$ python main.py

✨ Some magic here ✨
```

</div>

...It would be called like:

<div class="termy">

```console
$ magic-app

✨ Some magic here ✨
```

</div>

Having a standalone program like that allows setting up shell/tab completion.

The first step to be able to create an installable package like that is to use an explicit `typer.Typer()` app.

Later you can learn all the process to create a standalone CLI application and [Build a Package](./package.md){.internal-link target=_blank}.

But for now, it's just good to know that you are on that path. 😎
