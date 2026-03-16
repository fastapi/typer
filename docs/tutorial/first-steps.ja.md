# はじめの一歩

## もっともシンプルな例

もっともシンプルな **Typer** のファイルは、次のようになります。

{* docs_src/first_steps/tutorial001_py310.py *}

これを `main.py` というファイルにコピーしてください。

試してみましょう。

<div class="termy">

```console
$ python main.py

Hello World

// ただ "Hello World" を表示するだけです。

// 次に --help を確認します
$ python main.py --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>main.py [OPTIONS]                            </b>
<b>                                                     </b>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                        Show this message   │
<font color="#A5A5A1">│                               and exit.           │</font>
<font color="#A5A5A1">╰───────────────────────────────────────────────────╯</font>
```

</div>

...とはいえ、このプログラムはまだあまり実用的ではありません。少し拡張してみましょう。

## **CLI argument** とは

ここでは **CLI argument** という言葉を、CLI アプリケーションに特定の順序で渡される **CLI parameters** を指すものとして使います。デフォルトでは *required* です。

ターミナルで次のように入力するとします。

<div class="termy">

```bash
$ ls ./myproject

first-steps.md  intro.md
```

</div>

`ls` は `./myproject` ディレクトリの内容を表示します。

* `ls` は *program*（または "command"、"CLI app"）です。
* `./myproject` は *CLI argument* で、この場合はディレクトリのパスを指しています。

これは、あとで出てくる **CLI options** とは少し異なります。

## CLI argument を追加する

前の例を、`name` という argument を受け取るように更新します。

{* docs_src/first_steps/tutorial002_py310.py hl[4,5] *}

<div class="termy">

```console

$ python main.py

// argument なしで実行すると、分かりやすいエラーが表示されます
<font color="#F4BF75">Usage: </font>main.py [OPTIONS] NAME
<font color="#A5A5A1">Try </font><font color="#44919F">&apos;main.py </font><font color="#44919F"><b>--help</b></font><font color="#44919F">&apos;</font><font color="#A5A5A1"> for help.</font>
<font color="#F92672">╭─ Error ───────────────────────────────────────────╮</font>
<font color="#F92672">│</font> Missing argument &apos;NAME&apos;.                          <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────╯</font>

// 次にその NAME CLI argument を渡します
$ python main.py Camila

Hello Camila

// ここで "Camila" が CLI argument です

// 同じ CLI argument に空白を含む名前を渡すには、引用符で囲みます
$ python main.py "Camila Gutiérrez"

Hello Camila Gutiérrez
```

</div>

/// tip

空白を含む 1 つの値を *CLI argument* に渡す必要がある場合は、引用符 (`"`) で囲んでください。

///

## 2 つの CLI argument

次は、名前と姓を分けて受け取りたいとします。

そこで、`name` と `lastname` の 2 つの argument を受け取るように拡張します。

{* docs_src/first_steps/tutorial003_py310.py hl[4,5] *}

<div class="termy">

```console
// main の --help を確認します
$ python main.py --help

<font color="#F4BF75">Usage: </font>main.py [OPTIONS] NAME
<font color="#A5A5A1">Try </font><font color="#44919F">&apos;main.py </font><font color="#44919F"><b>--help</b></font><font color="#44919F">&apos;</font><font color="#A5A5A1"> for help.</font>
<font color="#F92672">╭─ Error ───────────────────────────────────────────╮</font>
<font color="#F92672">│</font> Missing argument &apos;NAME&apos;.                          <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────╯</font>

<font color="#A1EFE4"><b>typer</b></font> on <font color="#AE81FF"><b> richify</b></font> <font color="#F92672"><b>[»!?] </b></font>via <font color="#F4BF75"><b>🐍 v3.7.5 (env3.7)</b></font>
<font color="#F92672"><b>❯</b></font> <font color="#A6E22E">python</font> <u style="text-decoration-style:single">main.py</u>
<font color="#F4BF75">Usage: </font>main.py [OPTIONS] NAME LASTNAME
<font color="#A5A5A1">Try </font><font color="#44919F">&apos;main.py </font><font color="#44919F"><b>--help</b></font><font color="#44919F">&apos;</font><font color="#A5A5A1"> for help.</font>
<font color="#F92672">╭─ Error ───────────────────────────────────────────╮</font>
<font color="#F92672">│</font> Missing argument &apos;NAME&apos;.                          <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────╯</font>

// これで CLI argument は 2 つ、name と lastname になりました

// 今度は name だけを 1 つ渡してみます
$ python main.py Camila

<font color="#F4BF75">Usage: </font>main.py [OPTIONS] NAME LASTNAME
<font color="#A5A5A1">Try </font><font color="#44919F">&apos;main.py </font><font color="#44919F"><b>--help</b></font><font color="#44919F">&apos;</font><font color="#A5A5A1"> for help.</font>
<font color="#F92672">╭─ Error ───────────────────────────────────────────╮</font>
<font color="#F92672">│</font> Missing argument &apos;LASTNAME&apos;.                      <font color="#F92672">│</font>
<font color="#F92672">╰───────────────────────────────────────────────────╯</font>

// この 2 つの argument は必須なので、両方渡します
$ python main.py Camila Gutiérrez

Hello Camila Gutiérrez
```

</div>

/// tip

順番が重要であることに注目してください。姓は名のあとに置く必要があります。

もし次のように呼び出すと:

```
$ python main.py Gutiérrez Camila
```

アプリはどちらが `name` でどちらが `lastname` かを判断できません。最初の *CLI argument* が `name`、2 番目の *CLI argument* が `lastname` であることを前提にしています。

///

## **CLI option** とは

ここでは **CLI option** という言葉を、特定の名前を使って CLI アプリケーションに渡す *CLI parameters* を指すものとして使います。たとえば、ターミナルで次のように入力するとします。

<div class="termy">

```console
$ ls ./myproject --size

12 first-steps.md   4 intro.md
```

</div>

`ls` は `./myproject` ディレクトリの内容を `size` 付きで表示します。

* `ls` は *program*（または "command"、"CLI app"）です。
* `./myproject` は *CLI argument* です。
* `--size` は省略可能な *CLI option* です。

プログラムは順序ではなく `--size` を見つけることで、サイズを表示すべきだと判断します。

`--size` のような *CLI option* は、*CLI argument* のように順番に依存しません。

そのため、*CLI argument* の *前* に `--size` を置いても動きます（実際には、それがもっとも一般的な書き方です）。

<div class="termy">

```console
$ ls --size ./myproject

12 first-steps.md   4 intro.md
```

</div>

*CLI option* と *CLI argument* の見た目上の主な違いは、*CLI option* には `--` が名前の前に付くことです。たとえば "`--size`" のようになります。

*CLI option* が順番に依存しないのは、事前に決まった名前を持っているからです（ここでは `--size`）。これは、CLI app がその特定の "name" を持つリテラルな `--size` parameter（"flag" や "switch" とも呼ばれます）を探しているためです。CLI app は、あなたが入力しなかった場合でも `--size` があるかどうかを確認します。

一方で、CLI app は文字列 "`./myproject`" を持つ *CLI argument* を積極的に探しているわけではありません。`./myproject` と入力するのか、`./my-super-awesome-project` と入力するのか、あるいはまったく別の値を入力するのかは事前に分からないからです。特定の *CLI argument* を指していると分かる唯一の手がかりは順番です。これは、最初の *CLI argument* が `name`、2 番目が `lastname` だと分かるのと同じです。順番を入れ替えると正しく扱えません。

対して、*CLI option* では順番は重要ではありません。

また、デフォルトでは *CLI option* は *optional*（*required* ではない）です。

そのため、デフォルトでは次のようになります。

* *CLI argument* は **required**
* *CLI option* は **optional**

ただし、*required* と *optional* のデフォルトは変更できます。

したがって、主な、そして **もっとも重要な** 違いは次のとおりです。

* *CLI options* は **`--` で始まり**、順番に依存しません
* *CLI arguments* は **並び順** に依存します

/// tip

上の例にある *CLI option* `--size` は、コマンドに追加されたかどうかに応じて `True` または `False` になる、単なる "flag" または "switch" です。

この例では値を受け取りません。しかし、*CLI options* も *CLI arguments* と同じように値を受け取れます。それについてはあとで見ていきます。

///

## 1 つの *CLI option* を追加する

次に、`--formal` という *CLI option* を追加します。

{* docs_src/first_steps/tutorial004_py310.py hl[4,5] *}

ここで `formal` は `bool` で、デフォルト値は `False` です。

<div class="termy">

```console
// help を取得します
$ python main.py --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>main.py [OPTIONS] NAME LASTNAME                            </b>
<b>                                                                   </b>
<font color="#A5A5A1">╭─ Arguments ─────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    name          <font color="#F4BF75"><b>TEXT</b></font>  [default: None] <font color="#A6194C">[required]</font>             │
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    lastname      <font color="#F4BF75"><b>TEXT</b></font>  [default: None] <font color="#A6194C">[required]</font>             │
<font color="#A5A5A1">╰─────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--formal</b></font>                <font color="#AE81FF"><b>--no-formal</b></font>      [default: no-formal]   │
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                                   Show this message and  │
<font color="#A5A5A1">│                                          exit.                  │</font>
<font color="#A5A5A1">╰─────────────────────────────────────────────────────────────────╯</font>
```

</div>

/// tip

`formal` が `bool` であることを検出したため、自動的に `--formal` と `--no-formal` の両方が作成される点に注目してください。

///
