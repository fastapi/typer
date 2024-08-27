# Exceptions and Errors

When your code has errors and you run it, it will show the error and an exception.

Typer does some tricks to help you detect those errors quickly.

## Example Broken App

Let's take this example broken app:

```Python hl_lines="5"
{!../docs_src/exceptions/tutorial001.py!}
```

This code is broken because you can't sum a string and a number (`name + 3`).

## Exceptions with Rich

If you have **Rich** installed (for example if you installed `"typer[all]"`), **Typer** will use it to automatically show you nicely printed errors.

It will **omit** all the parts of the traceback (the chain of things that called your function) that come from the internal parts in Typer and Click.

So, the error you see will be **much clearer** and simpler, to help you detect the problem in your code quickly:

<div class="termy">

```console
$ python main.py

<font color="#F92672">╭──────────────── </font><font color="#F92672"><b>Traceback (most recent call last)</b></font><font color="#F92672"> ────────────────╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><font color="#F4BF75"><b>main.py</b></font>:<font color="#66D9EF">5</font> in <font color="#A6E22E">main</font>                        <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>    2                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    3                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    4 <font color="#66D9EF">def</font> <font color="#A6E22E">main</font>(name: <font color="#A1EFE4">str</font> = <font color="#F4BF75">&quot;morty&quot;</font>):                               <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 5 │   <font color="#A1EFE4">print</font>(name + <font color="#66D9EF">3</font>)                                          <font color="#F92672">│</font>
<font color="#F92672">│</font>    6                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    7                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    8 <font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">&quot;__main__&quot;</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╭──── locals ────╮</font>                                                <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font> name = <font color="#F4BF75">&apos;morty&apos;</font> <font color="#F4BF75">│</font>                                                <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╰────────────────╯</font>                                                <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>TypeError: </b></font>can only concatenate str <b>(</b>not <font color="#A6E22E">&quot;int&quot;</font><b>)</b> to str
```

</div>

## Exceptions without Rich

If you don't have Rich installed, Typer will still do some tricks to show you the information **as clearly as possible**:

<div class="termy">

```console
$ python main.py

Traceback (most recent call last):

  File "main.py", line 12, in <module>
    typer.run(main)

  File "main.py", line 8, in main
    print(name + 3)

TypeError: can only concatenate str (not "int") to str
```

</div>

## Disable Local Variables for Security

If your Typer application handles **delicate information**, for example a **password**, a **key**, a **token**, then it could be problematic if the automatic errors show the value in those <abbr title="a variable that lives only inside a function, its value is only visible inside of it">local variables</abbr>.

This would be relevant in particular if your CLI application is being run on some CI (continuous integration) system that is recording the logs.

The default errors above, when using Rich, show a section with:

```Python
name = 'morty'
```

In this case, `name` is a local variable, it comes from a parameter passed to the function.

But if it was something like a password, you would have liked to hide it.

In that case, you can create the `typer.Typer()` application explicitly and set the parameter `pretty_exceptions_show_locals=False`:

```Python hl_lines="3"
{!../docs_src/exceptions/tutorial002.py!}
```

And now when you run it, you will see the error without the local variables:

<div class="termy">

```console
$ python main.py supersecret

<font color="#F92672">╭──────────────── </font><font color="#F92672"><b>Traceback (most recent call last)</b></font><font color="#F92672"> ────────────────╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><font color="#F4BF75"><b>main.py</b></font>:<font color="#66D9EF">8</font> in <font color="#A6E22E">main</font>                        <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>    5                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    6 <font color="#AE81FF"><b>@app</b></font>.command()                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>    7 <font color="#66D9EF">def</font> <font color="#A6E22E">main</font>(password: <font color="#A1EFE4">str</font>):                                     <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 8 │   <font color="#A1EFE4">print</font>(password + <font color="#66D9EF">3</font>)                                      <font color="#F92672">│</font>
<font color="#F92672">│</font>    9                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   10                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   11 <font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">&quot;__main__&quot;</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>TypeError: </b></font>can only concatenate str <b>(</b>not <font color="#A6E22E">&quot;int&quot;</font><b>)</b> to str
```

</div>

Note that you passed the password `supersecret`, but it's not shown anywhere in the error message.

Being able to see the values of local variables is normally very **helpful** to diagnose, **debug**, and fix problems, but if you are dealing with delicate information, now you know how to secure it. 🔒

## Disable Short Output

If you want to show the full exception, including the parts in Typer and Click, you can use the parameter `pretty_exceptions_short=False`:

```Python hl_lines="3"
{!../docs_src/exceptions/tutorial003.py!}
```

Now when you run it, you will see the whole output:

<div class="termy">

```console
$ python main.py

<font color="#F92672">╭──────────────── </font><font color="#F92672"><b>Traceback (most recent call last)</b></font><font color="#F92672"> ────────────────╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><font color="#F4BF75"><b>main.py</b></font>:<font color="#66D9EF">12</font> in <font color="#A6E22E">&lt;module&gt;</font>                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>    9                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   10                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   11 <font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">&quot;__main__&quot;</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font>12 │   app()                                                    <font color="#F92672">│</font>
<font color="#F92672">│</font>   13                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╭─────────────────────────── locals ────────────────────────────╮</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font> <font color="#A6194C">__annotations__</font> = <b>{}</b>                                          <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>    <font color="#A6194C">__builtins__</font> = <b>&lt;</b><font color="#AE81FF"><b>module</b></font> <font color="#F4BF75">&apos;builtins&apos;</font> <b>(</b>built-in<b>)&gt;</b>              <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>      <font color="#A6194C">__cached__</font> = <font color="#66D9EF">None</font>                                        <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>         <font color="#A6194C">__doc__</font> = <font color="#66D9EF">None</font>                                        <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>        <font color="#A6194C">__file__</font> = <font color="#F4BF75">&apos;main.py&apos;</font>                                   <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>      <font color="#A6194C">__loader__</font> = <b>&lt;</b><font color="#AE81FF"><b>_frozen_importlib_external.SourceFileLoad…</b></font> <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>                   object at <font color="#66D9EF">0x7f047db1c050</font><b>&gt;</b>                   <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>        <font color="#A6194C">__name__</font> = <font color="#F4BF75">&apos;__main__&apos;</font>                                  <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>     <font color="#A6194C">__package__</font> = <font color="#66D9EF">None</font>                                        <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>        <font color="#A6194C">__spec__</font> = <font color="#66D9EF">None</font>                                        <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>             app = <b>&lt;</b><font color="#AE81FF"><b>typer.main.Typer</b></font> object at <font color="#66D9EF">0x7f047db51d90</font><b>&gt;</b> <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>            main = <b>&lt;</b><font color="#AE81FF"><b>function</b></font> main at <font color="#66D9EF">0x7f047db56830</font><b>&gt;</b>           <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>           typer = <b>&lt;</b><font color="#AE81FF"><b>module</b></font> <font color="#F4BF75">&apos;typer&apos;</font> from                        <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font>                   <font color="#F4BF75">&apos;/home/user/code/superapp/env/lib/python3.…</font> <font color="#F4BF75">│</font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╰───────────────────────────────────────────────────────────────╯</font> <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/typer/</font><font color="#F4BF75"><b>ma</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>in.py</b></font>:<font color="#66D9EF">328</font> in <font color="#A6E22E">__call__</font>                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/typer/</font><font color="#F4BF75"><b>ma</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>in.py</b></font>:<font color="#66D9EF">311</font> in <font color="#A6E22E">__call__</font>                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/click/</font><font color="#F4BF75"><b>co</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>re.py</b></font>:<font color="#66D9EF">1130</font> in <font color="#A6E22E">__call__</font>                                            <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/typer/</font><font color="#F4BF75"><b>co</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>re.py</b></font>:<font color="#66D9EF">723</font> in <font color="#A6E22E">main</font>                                                 <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/typer/</font><font color="#F4BF75"><b>co</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>re.py</b></font>:<font color="#66D9EF">216</font> in <font color="#A6E22E">_main</font>                                                <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/click/</font><font color="#F4BF75"><b>co</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>re.py</b></font>:<font color="#66D9EF">1404</font> in <font color="#A6E22E">invoke</font>                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/click/</font><font color="#F4BF75"><b>co</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>re.py</b></font>:<font color="#66D9EF">760</font> in <font color="#A6E22E">invoke</font>                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/env/lib/python3.7/site-packages/typer/</font><font color="#F4BF75"><b>ma</b></font> <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75"><b>in.py</b></font>:<font color="#66D9EF">683</font> in <font color="#A6E22E">wrapper</font>                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><font color="#F4BF75"><b>main.py</b></font>:<font color="#66D9EF">8</font> in <font color="#A6E22E">main</font>                        <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>    5                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    6 <font color="#AE81FF"><b>@app</b></font>.command()                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>    7 <font color="#66D9EF">def</font> <font color="#A6E22E">main</font>(name: <font color="#A1EFE4">str</font> = <font color="#F4BF75">&quot;morty&quot;</font>):                               <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 8 │   <font color="#A1EFE4">print</font>(name + <font color="#66D9EF">3</font>)                                          <font color="#F92672">│</font>
<font color="#F92672">│</font>    9                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   10                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   11 <font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">&quot;__main__&quot;</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╭──── locals ────╮</font>                                                <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">│</font> name = <font color="#F4BF75">&apos;morty&apos;</font> <font color="#F4BF75">│</font>                                                <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F4BF75">╰────────────────╯</font>                                                <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>TypeError: </b></font>can only concatenate str <b>(</b>not <font color="#A6E22E">&quot;int&quot;</font><b>)</b> to str
```

</div>


## Set Output Width

If you want to control the width of the yellow and red Rich exception borders, you can set the parameter `pretty_exceptions_width` to a specific integer
(by default it's the maximum console width if it can be determined, or otherwise 100):

```Python hl_lines="3"
{!../docs_src/exceptions/tutorial005.py!}
```

This prevents artificial line breaks in cases where there is sufficient horizontal space on the console.

## Disable Pretty Exceptions

You can also entirely disable pretty exceptions with the parameter `pretty_exceptions_enable=False`:

```Python hl_lines="3"
{!../docs_src/exceptions/tutorial004.py!}
```

And now you will see the full standard exception as with any other Python program:

<div class="termy">

```console
$ python main.py

Traceback (most recent call last):
  File "main.py", line 12, in <module>
    app()
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 328, in __call__
    raise e
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 311, in __call__
    return get_command(self)(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/core.py", line 723, in main
    **extra,
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/core.py", line 216, in _main
    rv = self.invoke(ctx)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 683, in wrapper
    return callback(**use_params)  # type: ignore
  File "main.py", line 8, in main
    print(name + 3)
TypeError: can only concatenate str (not "int") to str
```

</div>

You could also achieve the same with the environment variable `_TYPER_STANDARD_TRACEBACK=1`.

This will work for any other Typer program too, in case you need to debug a problem in a Typer program made by someone else:

<div class="termy">

```console
export _TYPER_STANDARD_TRACEBACK=1
$ python main.py


Traceback (most recent call last):
  File "main.py", line 12, in <module>
    app()
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 328, in __call__
    raise e
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 311, in __call__
    return get_command(self)(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/core.py", line 723, in main
    **extra,
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/core.py", line 216, in _main
    rv = self.invoke(ctx)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/click/core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "/home/user/code/superapp/env/lib/python3.7/site-packages/typer/main.py", line 683, in wrapper
    return callback(**use_params)  # type: ignore
  File "main.py", line 8, in main
    print(name + 3)
TypeError: can only concatenate str (not "int") to str
```

</div>
