What inspired **Typer**, how it compares to other alternatives and what it learned from them.

## Intro

**Typer** wouldn't exist if not for the previous work of others.

There have been many tools created before that have helped inspire its creation.

## Previous tools

### <a href="https://docs.python.org/3/library/argparse.html" class="external-link" target="_blank">`argparse`</a>

`argparse` is the Python standard library's module to write CLIs.

It provides a better alternative than reading the *CLI Parameters* as a `list` of `str` and parsing everything by hand.

!!! check "Inspired **Typer** to"
    Provide a better development experience than just reading *CLI Parameters* by hand.

### <a href="https://www.hug.rest/" class="external-link" target="_blank">Hug</a>

Hug is a library to create APIs and CLIs, it uses parameters in functions to declare the required data.

It inspired a lot of the ideas in **FastAPI** and **Typer**.

!!! check "Inspired **Typer** to"
    Use function parameters to declare *CLI Arguments* and *CLI Options* as it simplifies a lot the development experience.

### <a href="https://micheles.github.io/plac/" class="external-link" target="_blank">Plac</a>

Plac is another library to create CLIs using parameters in functions, similar to Hug.

!!! check "Inspired **Typer** to"
    Provide a simple way to use a function as a command line app, without having to create a complete app, with `typer.run(some_function)`.

### <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>

Pydantic is a library to handle data validation using standard modern Python type annotations.

It powers **FastAPI** underneath.

It is not used by **Typer**, but it inspired a lot of the design (through **FastAPI**).

!!! check "Inspired **Typer** to"
    Use standard Python type annotations to declare types instead of library-specific types or classes and use them for data validation and documentation.

### <a href="https://click.palletsprojects.com" class="external-link" target="_blank">Click</a>

Click is one of the most widely used libraries to create CLIs in Python.

It's a very powerful tool and there are many CLIs built with it. It is what powers **Typer** underneath.

It also uses functions with parameters for *CLI Arguments* and *CLI Options*, but the declaration of the specific *CLI Arguments*, *CLI Options*, types, etc, is done in decorators on top of the function. This requires some code repetition (e.g. a *CLI Option* name `--verbose` and a variable name `verbose`) and synchronization between two places related to the same information (the decorator and the parameter function).

It uses decorators on top of functions to modify the actual value of those functions, converting them to instances of a specific class. This is a clever trick, but code editors can't provide great support for autocompletion that way.

It was built with some great ideas and design using the features available in the language at the time (Python 2.x).

!!! check "**Typer** uses it for"
    Everything. 🚀

    **Typer** mainly adds a layer on top of Click, making the code simpler and easier to use, with autocompletion everywhere, etc, but providing all the powerful features of Click underneath.

    As someone pointed out: <em><a href="https://twitter.com/fishnets88/status/1210126833745838080" class="external-link" target="_blank">"Nice to see it is built on Click but adds the type stuff. Me gusta!"</a></em>

### <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a>

I created **FastAPI** to provide an easy way to build APIs with autocompletion for everything in the code (and some other <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">features</a>).

**Typer** is the "FastAPI of CLIs".

It uses the same design and usage of FastAPI as much as possible. So, if you have used FastAPI, you know how to use Typer.
