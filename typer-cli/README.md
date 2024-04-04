<p align="center">
  <a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" alt="Typer"></a>
</p>
<p align="center">
    <em>Typer, build great CLIs. Easy to code. Based on Python type hints.</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/typer/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/typer/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/tiangolo/typer/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/typer/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/typer" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/typer.svg" alt="Coverage">
<a href="https://pypi.org/project/typer" target="_blank">
    <img src="https://img.shields.io/pypi/v/typer?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://typer.tiangolo.com" target="_blank">https://typer.tiangolo.com/tutorial/typer-command/</a>

**Source Code**: <a href="https://github.com/tiangolo/typer" target="_blank">https://github.com/tiangolo/typer</a>

---

Typer is a library for building <abbr title="command line interface, programs executed from a terminal">CLI</abbr> applications that users will **love using** and developers will **love creating**. Based on Python type hints.

## Typer CLI

This package, `typer-cli`, only provides a command `typer` in the shell with the same functionality of `python -m typer`.

The only reason why this is a separate package is to allow developers to opt out of the `typer` command by installing `typer-slim`, that doesn't include `typer-cli`.

You probably **should not** install this package.

Install instead:

```bash
pip install typer
```

That includes this package, `typer-cli`, with the `typer` command.

## License

This project is licensed under the terms of the MIT license.
