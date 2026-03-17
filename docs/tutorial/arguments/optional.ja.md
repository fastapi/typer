# 省略可能な CLI 引数

前に説明したとおり、*デフォルトでは*:

* *CLI オプション* は **省略可能**
* *CLI 引数* は **必須**

繰り返しになりますが、これは *デフォルトでの* 挙動であり、多くの CLI プログラムやシステムでの慣例でもあります。

ただし、これは変更できます。

実際には、**省略可能** な *CLI 引数* を持つほうが、**必須** の *CLI オプション* を持つよりもずっと一般的です。

それがどのように役立つかの例として、`ls` という CLI プログラムの動きを見てみましょう。

<div class="termy">

```console
// ただ入力すると
$ ls

// ls は現在のディレクトリ内のファイルとディレクトリを一覧表示します
typer  tests  README.md  LICENSE

// ただし、省略可能な CLI 引数も受け取れます
$ ls ./tests/

// すると ls は、その CLI 引数で指定されたディレクトリ内のファイルとディレクトリを一覧表示します
__init__.py  test_tutorial
```

</div>

## *CLI 引数* の別の宣言方法

[First Steps](../first-steps.md#add-a-cli-argument){.internal-link target=_blank} では、*CLI 引数* を追加する方法を見ました。

{* docs_src/first_steps/tutorial002_py310.py hl[4] *}

ここで、同じ *CLI 引数* を作る別の方法を見てみましょう。

{* docs_src/arguments/optional/tutorial000_an_py310.py hl[6] *}

あるいは、`Typer()` instance を明示的に作る形では次のようになります。

{* docs_src/arguments/optional/tutorial001_an_py310.py hl[9] *}

/// info

Typer はバージョン 0.9.0 で `Annotated` のサポートを追加し、以後それを推奨するようになりました。

それより古いバージョンを使っている場合、`Annotated` を使おうとするとエラーになります。

`Annotated` を使う前に、Typer のバージョンを少なくとも 0.9.0 へ更新してください。

///

以前は、次のような関数パラメータでした。

```Python
name: str
```

それを今度は `Annotated` で包みます。

```Python
name: Annotated[str]
```

この 2 つは同じ意味で、`Annotated` はそのために標準 Python に用意されています。

ただし `Annotated` を使う後者の書き方では、**Typer** が利用できる追加のメタデータを渡せます。

```Python
name: Annotated[str, typer.Argument()]
```

これで `name` が *CLI 引数* であることを明示しています。型は依然として `str` のままで、デフォルト値を持たないので必須のままです。

ここでやっていることは、以前と同じ **必須** の *CLI 引数* を作ることです。

<div class="termy">

```console
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.
```

</div>

まだそれほど便利ではありませんが、正しく動作しています。

そして、

```Python
name: Annotated[str, typer.Argument()]
```

のように **必須** の *CLI 引数* を宣言する方法は、

```Python
name: str
```

とまったく同じように動きます。

これはあとで役立ちます。

## *CLI 引数* を省略可能にする

さて、ここで本題の、省略可能な *CLI 引数* を見ていきます。

*CLI 引数* を省略可能にするには、`typer.Argument()` を使い、"default" 値を与えます。たとえば `"World"` のようにします。

{* docs_src/arguments/optional/tutorial002_an_py310.py hl[9] *}

これで次のようになります。

```Python
name: Annotated[str, typer.Argument()] = "World"
```

`typer.Argument()` を使っているので、**Typer** はこれが *CLI 引数* だと分かります（*必須* か *省略可能* かに関係なく）。

help を確認してみましょう。

<div class="termy">

```console
// まず help を確認します
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]

Options:
  --help                Show this message and exit.
```

</div>

/// tip

`NAME` は依然として *CLI 引数* であり、"`Usage: main.py` ..." の部分に表示されていることに注目してください。

また、以前は単に `NAME` だったのに対し、今は `[NAME]` のように角括弧で囲まれていて、これが **必須** ではなく **省略可能** であることを表しています。

///

では、実行して試してみましょう。

<div class="termy">

```console
// CLI 引数なし
$ python main.py

Hello World!

// 省略可能な CLI 引数を 1 つ渡す
$ python main.py Camila

Hello Camila
```

</div>

/// tip

ここでの "`Camila`" は、省略可能な *CLI 引数* であって *CLI オプション* ではありません。"`--name Camila`" のような形ではなく、単に "`Camila`" をプログラムへ直接渡しているからです。

///

## 古い別方式: `typer.Argument()` をデフォルト値として使う

**Typer** は、追加のメタデータ付きで *CLI 引数* を宣言する、もう 1 つの古い書き方もサポートしています。

`Annotated` を使う代わりに、`typer.Argument()` をデフォルト値として使えます。

{* docs_src/arguments/optional/tutorial001_py310.py hl[7] *}

/// tip

可能なら `Annotated` 版を使うほうがよいです。

///

以前は、`name` にデフォルト値がなかったので、Python の意味では **必須パラメータ** でした。

デフォルト値として `typer.Argument()` を使うと、**Typer** も同様にこれを **必須** の *CLI 引数* として扱います。

次のように変更しました。

```Python
name: str = typer.Argument()
```

しかし、今度は `typer.Argument()` が関数パラメータの「デフォルト値」になるため、Python の意味では「もはや必須ではない」ことになります。

関数パラメータに Python 側のデフォルト値があるかどうかで必須性やデフォルト値を判断できなくなるため、`typer.Argument()` は最初の引数として `default` パラメータを受け取り、それで同じ目的を果たします。

`default` 引数に何も渡さないのは、必須として扱うのと同じです。ただし `typer.Argument(default=...)` のように `...` を渡して、明示的に *required* とすることもできます。

```Python
name: str = typer.Argument(default=...)
```

/// info

もしこの `...` を見たことがなければ、それは特殊な単一の値で、<a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">Python に含まれる "Ellipsis"</a> です。

///

{* docs_src/arguments/optional/tutorial003_py310.py hl[7] *}

同様に、たとえば `"World"` のような別の `default` 値を渡せば、省略可能にできます。

{* docs_src/arguments/optional/tutorial002_py310.py hl[7] *}

`typer.Argument(default="World")` に渡した最初のパラメータ（新しい "default" 値）が `"World"` なので、**Typer** はこれを **省略可能** な *CLI 引数* だと判断します。コマンドラインで呼び出すときに値が与えられなければ、その `"World"` がデフォルト値として使われます。

`default` 引数は最初のものなので、`default=` を明示せずに値を渡しているコードを見ることもあるでしょう。たとえば次のような形です。

```Python
name: str = typer.Argument(...)
```

あるいは次のような形です。

```Python
name: str = typer.Argument("World")
```

ただし繰り返しになりますが、可能なら `Annotated` を使うようにしてください。そのほうが Python の意味としても **Typer** の意味としても同じになり、こうした細部を覚えなくて済みます。
