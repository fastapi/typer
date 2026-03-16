# Typer App

## 明示的な application

ここまでは、1 つの関数を作って、その関数を `typer.run()` に渡す方法を見てきました。

たとえば次のような形です。

{* docs_src/first_steps/tutorial002_py310.py hl[9] *}

ただし、これは実際にはショートカットです。内部では **Typer** がそれを `typer.Typer()` を使った CLI application に変換し、実行しています。これらはすべて `typer.run()` の中で行われています。

同じことを実現する、より明示的な書き方もあります。

{* docs_src/typer_app/tutorial001_py310.py hl[3,6,12] *}

`typer.run()` を使うとき、**Typer** はだいたい次のようなことをしています。

* 新しい `typer.Typer()` の "application" を作成する
* あなたの関数から新しい "`command`" を作成する
* その同じ "application" を "`app()`" のように関数として呼び出す

/// info | `@decorator` Info

Python における `@something` という構文は "decorator" と呼ばれます。

関数の上に置く構文です。飾りのついた帽子のようなものだと考えてください（たぶん、そこからこの名前が来ています）。

"decorator" は、その下にある関数を受け取り、何らかの処理を行います。

ここでの decorator は、下の関数が "`command`" であることを **Typer** に伝えています。
commands については、後ほど [commands](./commands/index.md){.internal-link target=_blank} セクションでもっと詳しく学びます。

///

`typer.run()` を使う方法も、明示的に application を作る方法も、ほぼ同じ結果になります。

/// tip

もし `typer.run()` だけで要件を満たせるなら、それで問題ありません。明示的な `app` を作って `@app.command()` などを使う必要はありません。

あとでアプリに追加機能が必要になったらその方法を使いたくなるかもしれませんが、まだ必要でなければそれで十分です。

///

2 番目の例、つまり明示的な `app` を使う例を実行すると、動作はまったく同じです。

<div class="termy">

```console
// CLI argument なし
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.

// NAME CLI argument あり
$ python main.py Camila

Hello Camila

// help を求める
$ python main.py  --help

Usage: main.py [OPTIONS] NAME

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## CLI application completion

ここで注目しておく価値のある小さなポイントがあります。

help に 2 つの新しい *CLI options* が表示されるようになりました。

* `--install-completion`
* `--show-completion`

shell/tab completion を使うには、自分や利用者がインストールできて、**直接呼び出せる** package を作る必要があります。

つまり、次のように Python script を実行する代わりに:

<div class="termy">

```console
$ python main.py

✨ Some magic here ✨
```

</div>

...次のように呼び出せるようにする、ということです。

<div class="termy">

```console
$ magic-app

✨ Some magic here ✨
```

</div>

そのような standalone program にすることで、shell/tab completion をセットアップできるようになります。

インストール可能な package を作成するための最初のステップは、明示的な `typer.Typer()` app を使うことです。

install 可能な standalone CLI application を作る一連の流れについては、あとで [Build a Package](./package.md){.internal-link target=_blank} で学べます。

ただ、今の段階では、自分がその道の上にいると分かっていれば十分です。 😎
