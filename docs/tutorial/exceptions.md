# Exceptions and Errors

When your code has errors and you run it, it will show the error and an exception.

Typer does some tricks to help you detect those errors quickly.

## Example Broken App

Let's take this example broken app:

{* docs_src/exceptions/tutorial001_py39.py hl[8] *}

This code is broken because you can't sum a string and a number (`name + 3`).

## Exceptions with Rich

**Typer** will automatically use Rich to automatically show you nicely printed errors.

It will **omit** all the parts of the traceback (the chain of things that called your function) that come from the internal parts in Typer.

So, the error you see will be **much clearer** and simpler, to help you detect the problem in your code quickly:

<div class="termy">

```console
$ python main.py

<font color="#F92672">╭──────────────── </font><font color="#F92672"><b>Traceback (most recent call last)</b></font><font color="#F92672"> ────────────────╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><font color="#F4BF75"><b>main.py</b></font>:<font color="#66D9EF">8</font> in <font color="#A6E22E">main</font>                        <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>    5                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    6 <font color="#FF00FF">@app</font>.command()                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>    7 <font color="#66D9EF">def</font> <font color="#A6E22E">main</font>(name: <font color="#A1EFE4">str</font> = <font color="#F4BF75">&quot;morty&quot;</font>):                               <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 8 │   <font color="#A1EFE4">print</font>(name + <font color="#66D9EF">3</font>)                                          <font color="#F92672">│</font>
<font color="#F92672">│</font>    9                                                              <font color="#F92672">│</font>
<font color="#F92672">│</font>    10                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>    11 <font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">&quot;__main__&quot;</font>:                                  <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>TypeError: </b></font>can only concatenate str <b>(</b>not <font color="#A6E22E">&quot;int&quot;</font><b>)</b> to str
```

</div>

## Exceptions without Rich

You can disable Rich globally using the environmental variable `TYPER_USE_RICH`.

In this case, Typer will still do some tricks to show you the information **as clearly as possible**:

<div class="termy">

```console
$ python main.py

Traceback (most recent call last):

  File "main.py", line 12, in <module>
    app()

  File "main.py", line 8, in main
    print(name + 3)

TypeError: can only concatenate str (not "int") to str
```

</div>

## Show Local Variables for Detailed Debugging

When using Rich, you can get more verbose output by printing the values of the <abbr title="a variable that lives only inside a function, its value is only visible inside of it">local variables</abbr> as part of the error message.

By default, this setting is disabled (since Typer 0.23.0) to avoid showing **delicate information**, for example a **password**, a **key** or a **token**.

In these cases, it could be problematic if the automatic errors show the value in those local variables.

This would be relevant in particular if your CLI application is being run on some CI (continuous integration) system that is recording the logs.

However, if you do want to enable the setting, you can set the parameter `pretty_exceptions_show_locals=True` when creating the `typer.Typer()` application:

{* docs_src/exceptions/tutorial002_py39.py hl[3] *}

Now, when using Rich, you will see the error with the local variables:

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

Being able to see the values of local variables is very **helpful** to diagnose, **debug**, and fix problems.

But you should only enable it if you're not dealing with delicate information.

## Disable Short Output

If you want to show the full exception, including the internal parts in Typer, you can use the parameter `pretty_exceptions_short=False`:

{* docs_src/exceptions/tutorial003_py39.py hl[3] *}

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

## Disable Pretty Exceptions

You can also entirely disable pretty exceptions with the parameter `pretty_exceptions_enable=False`:

{* docs_src/exceptions/tutorial004_py39.py hl[3] *}

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

You could also achieve the same with the environment variable `TYPER_STANDARD_TRACEBACK=1` (or by setting the deprecated variable `_TYPER_STANDARD_TRACEBACK=1`).

This will work for any other Typer program too, in case you need to debug a problem in a Typer program made by someone else:

<div class="termy">

```console
export TYPER_STANDARD_TRACEBACK=1
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
