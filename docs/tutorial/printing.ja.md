# 出力と色

画面に情報を表示するには、通常の `print()` を使えます。

{* docs_src/typer_app/tutorial001_py310.py hl[8] *}

通常どおり出力されます。

<div class="termy">

```console
$ python main.py World

Hello World
```

</div>

## Rich を使う

<a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> を使うと、より美しく、より複雑な情報も表示できます。`typer` をインストールすると、デフォルトで利用できます。

### Rich の `print` を使う

もっとも単純なケースでは、`rich` から `print` を import して、標準の `print` の代わりに使うだけです。

{* docs_src/printing/tutorial001_py310.py hl[2,18] *}

これだけで、**Rich** はデータをきれいな色と構造で出力できます。

<div class="termy">

```console
$ python main.py

Here's the data
<b>{</b>
    <font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Rick&apos;</font>,
    <font color="#A6E22E">&apos;age&apos;</font>: <font color="#A1EFE4"><b>42</b></font>,
    <font color="#A6E22E">&apos;items&apos;</font>: <b>[</b>
        <b>{</b><font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Portal Gun&apos;</font><b>}</b>,
        <b>{</b><font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Plumbus&apos;</font><b>}</b>
    <b>]</b>,
    <font color="#A6E22E">&apos;active&apos;</font>: <font color="#A6E22E"><i>True</i></font>,
    <font color="#A6E22E">&apos;affiliation&apos;</font>: <font color="#AE81FF"><i>None</i></font>
<b>}</b>
```

</div>

### Rich Markup

Rich は、色やスタイルを指定するための <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">独自のマークアップ構文</a> もサポートしています。たとえば次のように使えます。

{* docs_src/printing/tutorial002_py310.py hl[9] *}

<div class="termy">

```console
$ python main.py

<font color="#F92672"><b>Alert!</b></font> <font color="#A6E22E">Portal gun</font> shooting! 💥
```

</div>

この例では、フォントスタイル、色、さらには絵文字まで使えることが分かります。

詳しくは <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">Rich のドキュメント</a> を確認してください。

### Rich Tables

Rich は内部的には `Console` オブジェクトを使って情報を表示しています。

Rich の `print` を呼び出すと、自動的にこのオブジェクトが作成されて使われます。

ただし、より高度な用途では自分で `Console` を作成することもできます。

{* docs_src/printing/tutorial003_py310.py hl[2:3,5,12:15] *}

この例では、`Console` と `Table` を作成し、そこにいくつかの行を追加して出力しています。

実行すると、きれいに整形されたテーブルが表示されます。

<div class="termy">

```console
$ python main.py

┏━━━━━━━┳━━━━━━━━━━━━┓
┃<b> Name  </b>┃<b> Item       </b>┃
┡━━━━━━━╇━━━━━━━━━━━━┩
│ Rick  │ Portal Gun │
│ Morty │ Plumbus    │
└───────┴────────────┘
```

</div>

Rich には他にも多くの機能があります。たとえば次のドキュメントを確認できます。

* <a href="https://rich.readthedocs.io/en/stable/prompt.html" class="external-link" target="_blank">Prompt</a>
* <a href="https://rich.readthedocs.io/en/stable/markdown.html" class="external-link" target="_blank">Markdown</a>
* <a href="https://rich.readthedocs.io/en/stable/panel.html" class="external-link" target="_blank">Panel</a>
* ...and more.

### Typer と Rich

どの用途にどのツールを使うべきか気になるなら、**Typer** は option、argument、subcommand、データ検証などを含めてコマンドラインアプリケーションを構成するのに向いています。

一般に **Typer** は、利用者から最初の入力を受け取る、プログラムの入口になりやすいです。

**Rich** は、情報を *表示* する部分に向いています。画面に美しい内容を表示するためのものです。

最良のコマンドラインアプリケーションは、**Typer** と **Rich** を組み合わせることで実現できます。

## "Standard Output" と "Standard Error"

出力の仕組みを内部から見ると、**オペレーティングシステム**（Linux、Windows、macOS）は、CLI プログラムが "**standard output**" という "**仮想ファイル**" に **文字列を書き込んでいる** かのように扱います。

コードが何かを "print" するとき、実際にはこの "standard output" という "仮想ファイル" に "書き込み" を行っています。

奇妙に思えるかもしれませんが、CLI プログラムとオペレーティングシステムはこのようにやり取りしています。

そしてオペレーティングシステムは、CLI プログラムがその "**standard output**" という "**仮想ファイル**" に "**書き込んだ**" ものを **画面に表示** します。

### Standard Error

また、通常はエラー専用に使われる "**standard error**" という別の "**仮想ファイル**" もあります。

ただし、"standard error" にも "print" できます。そして、そのどちらもターミナル上で利用者に表示されます。

/// info

PowerShell を使っている場合、"standard error" に出力した内容はターミナルに表示されないことがあります。

PowerShell では "standard error" を見るには変数 `$Error` を確認する必要があります。

ただし Bash、Zsh、Fish では通常どおり動作します。

///

### "standard error" に出力する

Rich の `Console` を `stderr=True` で作成すると、"standard error" に出力できます。

/// tip

`stderr` は "standard error" の略です。

///

`stderr=True` を使うと、出力を "standard error" に表示するよう **Rich** に伝えられます。

{* docs_src/printing/tutorial004_py310.py hl[4,11] *}

ターミナルで試すと、おそらく見た目は同じです。

<div class="termy">

```console
$ python main.py

Here is something written to standard error
```

</div>

## "Standard Input"

最後にもう 1 つ細かい点として、ターミナルでキーボードから文字を入力するとき、オペレーティングシステムはそれも、あなたが文字列を書き込んでいる別の "**仮想ファイル**" とみなします。

この仮想ファイルは "**standard input**" と呼ばれます。

### これは何のためか

今のところ、これはあまり役に立たないように思えるかもしれません 🤷‍♂。

でも、これを理解しておくと、たとえば autocompletion やテストの場面で後々役に立ちます。

## Typer Echo

/// warning

多くの場合、高度な情報を表示するには <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> を使うことをおすすめします。

このセクションの残りは、おそらく読み飛ばしても大丈夫です。 🎉😎

///

**Typer** にも、画面へ情報を出力するための小さなユーティリティ `typer.echo()` があります。ただし、通常はこれを使う必要はありません。

もっとも単純なケースでは、標準の Python `print()` を使えます。

そして、よりきれいにデータを表示したい場合や、より高度な内容を表示したい場合は、その代わりに **Rich** を使うべきです。

### なぜ `typer.echo` があるのか

`typer.echo()`（実体はただの `click.echo()` です）は、バイナリデータを文字列に変換しようとしたり、そのほかの似た処理を行ったりするためのチェックをいくつか適用します。

ただし、たいていの場合はその必要はありません。現代の Python では文字列（`str`）はすでに Unicode をサポートしており、画面に表示したい純粋な `bytes` を直接扱うことはほとんどないからです。

もし `bytes` オブジェクトがあるなら、出力しようとする前に、意図的かつ直接 decode したくなる場合がほとんどでしょう。

そして、色やその他の機能付きでデータを表示したいなら、**Rich** のより高度なツールを使うほうがずっと適しています。

### 色

/// note | Technical Details

ターミナルで色が機能する仕組みは、文字列の一部としていくつかのコード（ANSI escape sequences）を使うことです。

そのため、色付き文字列も依然として単なる `str` です。

///

/// tip

繰り返しになりますが、これについても <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> を使うほうがずっと適しています。 😎

///

`typer.style()` を使うと、ターミナルに出力できる色付き文字列を作成できます。そして、その `str` を `typer.echo()` に渡せます。

{* docs_src/printing/tutorial005_py310.py hl[10,12] *}

/// tip

パラメータ `fg` と `bg` には、"<strong>f</strong>ore<strong>g</strong>round" と "<strong>b</strong>ack<strong>g</strong>round" の色名を表す文字列を渡します。単純に `fg="green"` や `bg="red"` を渡すこともできます。

ただし **Typer** は、それらを `typer.colors.GREEN` のような変数としても提供しています。色を選ぶときに autocompletion を使えるようにするためです。

///

確認してみましょう。

<div class="use-termynal" data-termynal>
<span data-ty="input">python main.py</span>
<span data-ty>everything is <span style="color: green; font-weight: bold;">good</span></span>
<span data-ty="input">python main.py --no-good</span>
<span data-ty>everything is <span style="color: white; background-color: red;">bad</span></span>
</div>

`typer.style()` には次の関数引数を渡せます。

* `fg`: 前景色
* `bg`: 背景色
* `bold`: 太字表示を有効または無効にする
* `dim`: 薄い表示を有効または無効にする。これは十分にはサポートされていません
* `underline`: 下線を有効または無効にする
* `blink`: 点滅を有効または無効にする
* `reverse`: 反転表示を有効または無効にする（前景色と背景色が入れ替わります）
* `reset`: デフォルトでは、文字列の末尾に reset-all コードが追加され、スタイルが引き継がれないようになります。スタイルを組み合わせたい場合はこれを無効にできます

### `typer.secho()` - スタイル付きで出力する

/// tip

上で見落としていなければ分かるとおり、これについても <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> を使うほうがずっと適しています。 😎

///
