# Awesome CLI

Demo App

**Usage**:

```console
$ multiapp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

The end

**Commands**:

* `top`: Top command
* `sub`

## `multiapp top`

Top command

**Usage**:

```console
$ multiapp top [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `multiapp sub`

**Usage**:

```console
$ multiapp sub [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `hello`: Say Hello
* `hi`: Say Hi
* `bye`: Say bye

### `multiapp sub hello`

Say Hello

**Usage**:

```console
$ multiapp sub hello [OPTIONS]
```

**Options**:

* `--name <str>`: [default: World]
* `--age <int>`: The age of the user  [default: 0]
* `--help`: Show this message and exit.

### `multiapp sub hi`

Say Hi

**Usage**:

```console
$ multiapp sub hi [OPTIONS] [user]
```

**Arguments**:

* `[user]`: The name of the user to greet  [default: World]

**Options**:

* `--help`: Show this message and exit.

### `multiapp sub bye`

Say bye

**Usage**:

```console
$ multiapp sub bye [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
