# デフォルト値付き CLI 引数

同じ `typer.Argument()` を使ってデフォルト値を設定することもできます。

そうすると、その *CLI 引数* は省略可能になるだけでなく、デフォルト値も持つようになります。

## デフォルト値を持つ省略可能な *CLI 引数*

`typer.Argument()` を使って、*CLI 引数* に `None` 以外のデフォルト値を持たせることもできます。

{* docs_src/arguments/default/tutorial001_an_py310.py hl[9] *}

/// tip

この場合、値は利用者が渡す `str` か、デフォルト値 `"Wade Wilson"` のどちらかで、どちらも `str` です。したがって、値が `None` になることはないので、`Optional[str]` を使う必要はありませんし、使うべきでもありません。

`Optional[something]` は、Python に「その値は `None` になり得る」と伝えるものです。ただし `Optional` を使っても、Typer に対して値が必須かどうかを伝えることにはなりません。

///

確認してみましょう。

<div class="termy">

```console
// help を確認します
$ python main.py --help

// [default: Wade Wilson] ✨ に注目してください
Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [default: Wade Wilson]

Options:
  --help                Show this message and exit.

// 省略可能な CLI 引数なし
$ python main.py

Hello Wade Wilson

// CLI 引数を 1 つ渡す
$ python main.py Camila

Hello Camila
```

</div>

## 動的なデフォルト値

`default_factory` 引数に関数を渡せば、デフォルト値を動的に生成することもできます。

{* docs_src/arguments/default/tutorial002_an_py310.py hl[9:10,14] *}

この場合は、毎回ランダムな `str` を返す `get_name` 関数を作成しています。

そして、それを `typer.Argument()` の最初の関数引数として渡しています。

/// tip

`default_factory` の "factory" という言葉は、単に「デフォルト値を作る関数」という意味です。

///

確認してみましょう。

<div class="termy">

```console
// help を確認します
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [default: (dynamic)]

Options:
  --help                Show this message and exit.

// 何度か試してみてください。毎回ランダムなデフォルト値が使われます
$ python main.py

Hello Deadpool

$ python main.py

Hello Hiro

$ python main.py

Hello Rick

// 今度は CLI 引数に値を渡します
$ python main.py Camila

Hello Camila
```

</div>
