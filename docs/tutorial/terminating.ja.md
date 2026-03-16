# 終了する

ある時点で command を終了し、それ以降の実行をすべて止めたい場面があります。

コードがプログラムの正常終了を判断した場合もあれば、処理が中断された場合もあるでしょう。

## CLI program を `Exit` する

通常は CLI program のコードを最後まで実行させれば十分ですが、シナリオによっては途中で終了したくなることがあります。そして、それ以降のコードが実行されないようにしたい場合もあります。

これは、必ずしもエラーを意味するわけではありません。単に、それ以上実行する必要がないだけです。

その場合は、`typer.Exit()` exception を raise できます。

{* docs_src/terminating/tutorial001_py310.py hl[9] *}

この例では、いくつか注目すべき点があります。

* CLI program は他の関数ではなく `main()` function です。*CLI argument* を受け取るのはこれです。
* `maybe_create_user()` function は、`typer.Exit()` を raise することで program を終了できます。
* `maybe_create_user()` によって program が終了した場合、`main()` 内の `send_new_user_notification()` は決して実行されません。

確認してみましょう。

<div class="termy">

```console
$ python main.py Camila

User created: Camila
Notification sent for new user: Camila

// 既存 user で試します
$ python main.py rick

The user already exists

// 通知用のコードは実行されず、2 つ目のメッセージは表示されないことに注目してください
```

</div>

/// tip

exception を raise していても、それが必ずしもエラーを意味するわけではありません。

これは "error" のように機能して、すべての実行を止められるため exception で実現されています。

ただしその後 **Typer** がそれを catch し、program を通常どおり終了させます。

///

## エラー付きで終了する

`typer.Exit()` は、省略可能な `code` parameter を受け取ります。デフォルトでは `code` は `0` で、エラーがなかったことを意味します。

`0` 以外の数値を `code` として渡すと、program の実行中にエラーがあったことを terminal に伝えられます。

{* docs_src/terminating/tutorial002_py310.py hl[10] *}

確認してみましょう。

<div class="termy">

```console
$ python main.py Camila

New user created: Camila

// 最後に実行した program の result code を表示します
$ echo $?

0

// 今度はエラー付きで終了させます
$ python main.py root

The root user is reserved

// 最後に実行した program の result code を表示します
$ echo $?

1

// 1 はエラーあり、0 はエラーなしを意味します。
```

</div>

/// tip

この error code は、あなたの CLI program を実行する別の program（たとえば Bash script）から使われることがあります。

///

## Abort

program を "abort" するために使える特別な exception があります。

これは `typer.Exit()` とほぼ同じように動作しますが、画面に `"Aborted!"` を表示します。実行が中断されたことを明示したい場合に、あとで役立つことがあります。

{* docs_src/terminating/tutorial003_py310.py hl[10] *}

確認してみましょう。

<div class="termy">

```console
$ python main.py Camila

New user created: Camila

// 今度はエラー付きで終了させます
$ python main.py root

The root user is reserved
Aborted!
```

</div>
