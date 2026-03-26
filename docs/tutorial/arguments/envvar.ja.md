# 環境変数付き CLI 引数

*CLI 引数* がコマンドラインで渡されなかった場合に、環境変数から値を読むよう設定することもできます。

/// tip

環境変数について詳しくは、[Environment Variables](../../environment-variables.md){.internal-link target=_blank} を参照してください。

///

そのためには、`typer.Argument()` の `envvar` パラメータを使います。

{* docs_src/arguments/envvar/tutorial001_an_py310.py hl[9] *}

この場合、*CLI 引数* `name` のデフォルト値は `"World"` ですが、コマンドラインで値が渡されなければ、環境変数 `AWESOME_NAME` に設定された値も読み取ります。

<div class="termy">

```console
// help を確認
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [env var: AWESOME_NAME;default: World]

Options:
  --help                Show this message and exit.

// CLI 引数なしで実行
$ python main.py

Hello Mr. World

// 今度は CLI 引数を渡す
$ python main.py Czernobog

Hello Mr. Czernobog

// 次に環境変数を使う
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday

// CLI 引数は env var より優先される
$ AWESOME_NAME=Wednesday python main.py Czernobog

Hello Mr. Czernobog
```

</div>

## 複数の環境変数

環境変数は 1 つに限りません。コマンドラインで値が渡されなかったときに使える環境変数のリストを宣言できます。

{* docs_src/arguments/envvar/tutorial002_an_py310.py hl[10] *}

確認してみましょう。

<div class="termy">

```console
// help を確認
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [env var: AWESOME_NAME, GOD_NAME;default: World]

Options:
  --help                Show this message and exit.

// 1 つ目の env var を試す
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday

// 2 つ目の env var を試す
$ GOD_NAME=Anubis python main.py

Hello Mr. Anubis
```

</div>

## help テキストから env var を隠す

デフォルトでは、使用される環境変数は help テキストに表示されますが、`show_envvar=False` で無効にできます。

{* docs_src/arguments/envvar/tutorial003_an_py310.py hl[11] *}

確認してみましょう。

<div class="termy">

```console
// help を確認
$ python main.py --help

// env var は表示されない
Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [default: World]

Options:
  --help                Show this message and exit.

// それでも env var は使える
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday
```

</div>
