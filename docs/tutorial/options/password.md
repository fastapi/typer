# Password CLI Option and Confirmation Prompt

Apart from having a prompt, you can make a *CLI option* have a `confirmation_prompt=True`:

//// tab | Python 3.7+

```Python hl_lines="7"
{!> ../docs_src/options/password/tutorial001_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="5"
{!> ../docs_src/options/password/tutorial001.py!}
```

////

And the CLI program will ask for confirmation:

<div class="termy">

```console
$ python main.py Camila

// It prompts for the email
# Email: $ camila@example.com
# Repeat for confirmation: $ camila@example.com

Hello Camila, your email is camila@example.com
```

</div>

## A Password prompt

When receiving a password, it is very common (in most shells) to not show anything on the screen while typing the password.

The program will still receive the password, but nothing will be shown on screen, not even `****`.

You can achieve the same using `hide_input=True`.

And if you combine it with `confirmation_prompt=True` you can easily receive a password with double confirmation:

//// tab | Python 3.7+

```Python hl_lines="8"
{!> ../docs_src/options/password/tutorial002_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="6-8"
{!> ../docs_src/options/password/tutorial002.py!}
```

////

Check it:

<div class="termy">

```console
$ python main.py Camila

// It prompts for the password, but doesn't show anything when you type
# Password: $
# Repeat for confirmation: $

// Let's imagine the password typed was "typerrocks"
Hello Camila. Doing something very secure with password.
...just kidding, here it is, very insecure: typerrocks
```

</div>
