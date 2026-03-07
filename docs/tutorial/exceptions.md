# Exceptions and Errors

When your code has errors and you run it, it will show the error and an exception.

Typer does some tricks to help you detect those errors quickly.

## Example Broken App

Let's take this example broken app:

{* docs_src/exceptions/tutorial001_py310.py hl[8] *}

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

{* docs_src/exceptions/tutorial002_py310.py hl[3] *}

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

{* docs_src/exceptions/tutorial003_py310.py hl[3] *}

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

## Disable Tracebacks From Certain Modules

If you are developing with Python frameworks other than **Typer**, you might get
long, verbose tracebacks through other people's code. This could make it
annoying to find the line in your own code that triggered the exception. And
seeing internal Python code from someone else's package is almost never helpful
when you're trying to troubleshoot your own code.

With pretty exceptions, you can use the parameter `pretty_exceptions_suppress`,
which takes a list of Python modules, or `str` paths. This indicates the modules
for which the **Rich** traceback formatter should suppress the traceback
details. Only filename and line number will be shown for these modules, but no
code or variables.

For example, calling `urllib.request.urlopen()` with an unknown URL protocol will
produce an exception with many internal stack frames from `urllib.request` that
you probably don't care about. It could look like this:

<div class="termy">

```console
$ python main.py

<font color="#F92672">╭─</font><font color="#F92672">───────────────</font><font color="#F92672"> </font><font color="#F92672"><b>Traceback </b></font><font color="#F92672">(most recent call last)</font><font color="#F92672"> </font><font color="#F92672">───────────────</font><font color="#F92672">─╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><b>main.py</b>:10 in main                       <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 7 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 8 </font><font color="#ff00ff"><b>@app</b></font>.command()                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 9 </font><font color="#66D9EF">def</font><font color="#A37F4E"> </font><font color="#A6E22E">main</font>():                                                  <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font>10 <font color="#A37F4E">│   </font>urllib.request.urlopen(<font color="#F4BF75">"</font><font color="#F4BF75">unknown://example.com</font><font color="#F4BF75">"</font>)          <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">11 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">12 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">13 </font><font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">"</font><font color="#F4BF75">__main__</font><font color="#F4BF75">"</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:216 in urlopen                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 213 </font><font color="#A37F4E">│   │   </font>_opener = opener = build_opener()                  <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 214 </font><font color="#A37F4E">│   </font><font color="#66D9EF">else</font>:                                                  <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 215 </font><font color="#A37F4E">│   │   </font>opener = _opener                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 216 <font color="#A37F4E">│   </font><font color="#66D9EF">return</font> opener.open(url, data, timeout)                 <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 217 </font>                                                           <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 218 </font><font color="#66D9EF">def</font><font color="#A37F4E"> </font><font color="#A6E22E">install_opener</font>(opener):                                <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 219 </font><font color="#A37F4E">│   </font><font color="#66D9EF">global</font> _opener                                         <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:519 in open                      <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 516 </font><font color="#A37F4E">│   │   │   </font>req = meth(req)                                <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 517 </font><font color="#A37F4E">│   │   </font>                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 518 </font><font color="#A37F4E">│   │   </font>sys.audit(<font color="#F4BF75">'</font><font color="#F4BF75">urllib.Request</font><font color="#F4BF75">'</font>, req.full_url, req.data <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 519 <font color="#A37F4E">│   │   </font>response = <font color="#A1EFE4">self</font>._open(req, data)                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 520 </font><font color="#A37F4E">│   │   </font>                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 521 </font><font color="#A37F4E">│   │   </font><font color="#A37F4E"># post-process response</font>                            <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 522 </font><font color="#A37F4E">│   │   </font>meth_name = protocol+<font color="#F4BF75">"</font><font color="#F4BF75">_response</font><font color="#F4BF75">"</font>                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:536 in _open                     <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 533 </font><font color="#A37F4E">│   │   │   </font><font color="#66D9EF">return</font> result                                  <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 534 </font><font color="#A37F4E">│   │   </font>                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 535 </font><font color="#A37F4E">│   │   </font>protocol = req.type                                <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 536 <font color="#A37F4E">│   │   </font>result = <font color="#A1EFE4">self</font>._call_chain(<font color="#A1EFE4">self</font>.handle_open, protoc <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 537 </font><font color="#A37F4E">│   │   │   │   │   │   │   │     </font><font color="#F4BF75">'</font><font color="#F4BF75">_open</font><font color="#F4BF75">'</font>, req)            <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 538 </font><font color="#A37F4E">│   │   </font><font color="#66D9EF">if</font> result:                                         <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 539 </font><font color="#A37F4E">│   │   │   </font><font color="#66D9EF">return</font> result                                  <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:496 in _call_chain               <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 493 </font><font color="#A37F4E">│   │   </font>handlers = chain.get(kind, ())                     <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 494 </font><font color="#A37F4E">│   │   </font><font color="#66D9EF">for</font> handler <font color="#ff00ff">in</font> handlers:                           <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 495 </font><font color="#A37F4E">│   │   │   </font>func = <font color="#A1EFE4">getattr</font>(handler, meth_name)             <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font> 496 <font color="#A37F4E">│   │   │   </font>result = func(*args)                           <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 497 </font><font color="#A37F4E">│   │   │   </font><font color="#66D9EF">if</font> result <font color="#ff00ff">is</font> <font color="#ff00ff">not</font> <font color="#66D9EF">None</font>:                         <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 498 </font><font color="#A37F4E">│   │   │   │   </font><font color="#66D9EF">return</font> result                              <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 499 </font>                                                           <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:1419 in unknown_open             <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1416 </font><font color="#66D9EF">class</font><font color="#A37F4E"> </font><font color="#A6E22E">UnknownHandler</font>(BaseHandler):                         <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1417 </font><font color="#A37F4E">│   </font><font color="#66D9EF">def</font><font color="#A37F4E"> </font><font color="#A6E22E">unknown_open</font>(<font color="#A1EFE4">self</font>, req):                           <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1418 </font><font color="#A37F4E">│   │   </font><font color="#A1EFE4">type</font> = req.type                                    <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font>1419 <font color="#A37F4E">│   │   </font><font color="#66D9EF">raise</font> URLError(<font color="#F4BF75">'</font><font color="#F4BF75">unknown url type: </font><font color="#F4BF75">%s</font><font color="#F4BF75">'</font> % <font color="#A1EFE4">type</font>)      <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1420 </font>                                                           <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1421 </font><font color="#66D9EF">def</font><font color="#A37F4E"> </font><font color="#A6E22E">parse_keqv_list</font>(l):                                    <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">1422 </font><font color="#A37F4E">│   </font><font color="#F4BF75">"""Parse list of key=value strings where keys are not </font> <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>URLError: </b></font><b>&lt;</b><font color="#ff00ff"><b>urlopen</b></font> error unknown url type: unknown<b>&gt;</b>
```

</div>

That's a lot of clutter from `urllib.request` internals! You can suppress those
parts of the traceback with `pretty_exceptions_suppress`:

{* docs_src/exceptions/tutorial005_py310.py hl[5] *}

And now the traceback only shows your own code with full detail, while the
`urllib.request` frames are reduced to just a filename and line number:

<div class="termy">

```console
$ python main.py

<font color="#F92672">╭─</font><font color="#F92672">──────────────</font><font color="#F92672"> </font><font color="#F92672"><b>Traceback </b></font><font color="#F92672">(most recent call last)</font><font color="#F92672"> </font><font color="#F92672">────────────────</font><font color="#F92672">─╮</font>
<font color="#F92672">│</font> <font color="#A37F4E">/home/user/code/superapp/</font><b>main.py</b>:10 in main                       <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 7 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 8 </font><font color="#ff00ff"><b>@app</b></font>.command()                                               <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E"> 9 </font><font color="#66D9EF">def</font><font color="#A37F4E"> </font><font color="#A6E22E">main</font>():                                                  <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#F92672">❱ </font>10 <font color="#A37F4E">│   </font>urllib.request.urlopen(<font color="#F4BF75">"</font><font color="#F4BF75">unknown://example.com</font><font color="#F4BF75">"</font>)          <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">11 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">12 </font>                                                             <font color="#F92672">│</font>
<font color="#F92672">│</font>   <font color="#A37F4E">13 </font><font color="#66D9EF">if</font> <font color="#F92672">__name__</font> == <font color="#F4BF75">"</font><font color="#F4BF75">__main__</font><font color="#F4BF75">"</font>:                                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:216 in urlopen                   <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:519 in open                      <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:536 in _open                     <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:496 in _call_chain               <font color="#F92672">│</font>
<font color="#F92672">│</font>                                                                   <font color="#F92672">│</font>
<font color="#F92672">│</font> <font color="#A37F4E">.../python3.10/urllib/</font><b>request.py</b>:1419 in unknown_open             <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#F92672"><b>URLError: </b></font><b>&lt;</b><font color="#ff00ff"><b>urlopen</b></font> error unknown url type: unknown<b>&gt;</b>
```

</div>

## Disable Pretty Exceptions

You can also entirely disable pretty exceptions with the parameter `pretty_exceptions_enable=False`:

{* docs_src/exceptions/tutorial004_py310.py hl[3] *}

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
