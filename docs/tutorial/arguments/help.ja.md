# help 付き CLI 引数

*First Steps* セクションでは、関数の <abbr title="ドキュメント用に使われる、関数内の最初の式として書かれた複数行文字列（どの変数にも代入されない）">docstring</abbr> に書くことで、CLI アプリやコマンドの help を追加する方法を見ました。

その最後の例は次のようなものでした。

{* docs_src/first_steps/tutorial006_py310.py *}

`typer.Argument()` の使い方も分かったので、今度は *CLI 引数* 自体に対する説明を追加してみましょう。

## *CLI 引数* に `help` テキストを追加する

`help` パラメータを使うと、*CLI 引数* に help テキストを追加できます。

{* docs_src/arguments/help/tutorial001_an_py310.py hl[9] *}

すると、自動生成される `--help` オプションで使われます。

<div class="termy">

```console
$ python main.py --help

// 下の Arguments セクションを見てください 🚀
Usage: main.py [OPTIONS] NAME

Arguments:
  NAME  The name of the user to greet  [required]

Options:
  --help                Show this message and exit.
```

</div>

## help テキストと docstring を組み合わせる

もちろん、この `help` は <abbr title="ドキュメント用に使われる、関数内の最初の式として書かれた複数行文字列（どの変数にも代入されない）">docstring</abbr> と組み合わせることもできます。

{* docs_src/arguments/help/tutorial002_an_py310.py hl[9:12] *}

`--help` オプションには、すべての情報がまとめて表示されます。

<div class="termy">

```console
$ python main.py --help

// docstring の help テキストと Arguments の両方が入っていることに注目してください 📝
Usage: main.py [OPTIONS] NAME

  Say hi to NAME very gently, like Dirk.

Arguments:
  NAME  The name of the user to greet  [required]

Options:
  --help                Show this message and exit.
```

</div>

## デフォルト値の help

`"World"` のように、*CLI 引数* にデフォルト値がある場合:

{* docs_src/arguments/help/tutorial003_an_py310.py hl[9] *}

そのデフォルト値が help テキストに表示されます。

<div class="termy">

```console
$ python main.py --help

// [default: World] が表示されていることに注目してください 🔍
Usage: main.py [OPTIONS] [NAME]

  Say hi to NAME very gently, like Dirk.

Arguments:
  [NAME]  Who to greet  [default: World]

Options:
  --help                Show this message and exit.
```

</div>

ただし、`show_default=False` を使えば、これを無効にできます。

{* docs_src/arguments/help/tutorial004_an_py310.py hl[11] *}

すると、デフォルト値は表示されません。

<div class="termy">

```console
$ python main.py --help

// 今は [default: World] がないことに注目してください 🔥
Usage: main.py [OPTIONS] [NAME]

  Say hi to NAME very gently, like Dirk.

Arguments:
  [NAME]  Who to greet

Options:
  --help                Show this message and exit.
```

</div>

## カスタムデフォルト文字列

同じ `show_default` で `bool` の代わりに独自の文字列を渡すと、help テキストに表示するデフォルト値をカスタマイズできます。

{* docs_src/arguments/help/tutorial005_an_py310.py hl[13] *}

すると、その文字列が help テキストで使われます。

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  Who to greet  [default: (Deadpoolio the amazing's name)]


Options:
  --help                Show this message and exit.

// 実際のデフォルト値 "Wade Wilson" ではなく "(Deadpoolio the amazing's name)" が表示されています
```

</div>

## カスタム help 名（`metavar`）

生成される help テキストで *CLI 引数* を表す表示名もカスタマイズできます。

デフォルトでは、宣言した名前と同じものが大文字で使われます。

つまり、次のように宣言すると:

```Python
name: str
```

次のように表示されます。

```
NAME
```

これを変更したい場合は、`typer.Argument()` の `metavar` パラメータを使います。

たとえば、デフォルトの `NAME` ではなく、小文字の `username` を使いたいとします。しかも、どこにでも ✨ emojis ✨ を入れたい場合:

{* docs_src/arguments/help/tutorial006_an_py310.py hl[9] *}

生成される help テキストでは、`NAME` の代わりに `✨username✨` が表示されます。

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] [✨username✨]

Arguments:
  [✨username✨]  [default: World]

Options:
  --help                Show this message and exit.
```

</div>

## *CLI 引数* の help パネル

`--help` オプションを使うときに、*CLI 引数* の help 情報を別々のパネルに分けて表示したい場合があります。

[Printing and Colors](../printing.md){.internal-link target=_blank} のドキュメントで説明したように Rich をインストールしていれば、`rich_help_panel` パラメータに表示先パネル名を指定できます。

{* docs_src/arguments/help/tutorial007_an_py310.py hl[12,16] *}

`--help` オプションを確認すると、`rich_help_panel` を設定していない *CLI 引数* 用に、デフォルトで `Arguments` というパネルが表示されます。

その後に、`rich_help_panel` パラメータでカスタムパネルを指定した *CLI 引数* 用の別パネルが表示されます。

<div class="termy">

```console
$ python main.py --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>main.py [OPTIONS] NAME [LASTNAME] [AGE]               </b>
<b>                                                                     </b>
 Say hi to NAME very gently, like Dirk.

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    name      <font color="#F4BF75"><b>TEXT</b></font>  Who to greet [default: None] <font color="#A6194C">[required]</font>      │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Secondary Arguments ─────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│   lastname      </font><font color="#A37F4E"><b>[LASTNAME]</b></font>  The last name                         │
<font color="#A5A5A1">│   age           </font><font color="#A37F4E"><b>[AGE]     </b></font>  The user's age                        │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                        Show this message and exit.         │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>

この例では、`Secondary Arguments` という名前のカスタム *CLI 引数* パネルを使っています。
