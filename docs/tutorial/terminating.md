# Terminating

There are some cases where you might want to terminate a command at some point, and stop all subsequent execution.

It could be that your code determined that the program completed successfully, or it could be an operation aborted.

## `Exit` a CLI program

You can normally just let the code of your CLI program finish its execution, but in some scenarios, you might want to terminate at some point in the middle of it. And prevent any subsequent code to run.

This doesn't have to mean that there's an error, just that nothing else needs to be executed.

In that case, you can raise a `typer.Exit()` exception:

```Python hl_lines="9"
{!../docs_src/terminating/tutorial001.py!}
```

There are several things to see in this example.

* The CLI program is the function `main()`, not the others. This is the one that takes a *CLI argument*.
* The function `maybe_create_user()` can terminate the program by raising `typer.Exit()`.
* If the program is terminated by `maybe_create_user()` then `send_new_user_notification()` will never execute inside of `main()`.

Check it:

<div class="termy">

```console
$ python main.py Camila

User created: Camila
Notification sent for new user: Camila

// Try with an existing user
$ python main.py rick

The user already exists

// Notice that the notification code was never run, the second message is not printed
```

</div>

/// tip

Even though you are raising an exception, it doesn't necessarily mean there's an error.

This is done with an exception because it works as an "error" and stops all execution.

But then **Typer** (actually Click) catches it and just terminates the program normally.

///

## Exit with an error

`typer.Exit()` takes an optional `code` parameter. By default, `code` is `0`, meaning there was no error.

You can pass a `code` with a number other than `0` to tell the terminal that there was an error in the execution of the program:

```Python hl_lines="7"
{!../docs_src/terminating/tutorial002.py!}
```

Check it:

<div class="termy">

```console
$ python main.py Camila

New user created: Camila

// Print the result code of the last program executed
$ echo $?

0

// Now make it exit with an error
$ python main.py root

The root user is reserved

// Print the result code of the last program executed
$ echo $?

1

// 1 means there was an error, 0 means no errors.
```

</div>

/// tip

The error code might be used by other programs (for example a Bash script) that execute your CLI program.

///

## Abort

There's a special exception that you can use to "abort" a program.

It works more or less the same as `typer.Exit()` but will print `"Aborted!"` to the screen and can be useful in certain cases later to make it explicit that the execution was aborted:

```Python hl_lines="7"
{!../docs_src/terminating/tutorial003.py!}
```

Check it:

<div class="termy">

```console
$ python main.py Camila

New user created: Camila

// Now make it exit with an error
$ python main.py root

The root user is reserved
Aborted!
```

</div>
