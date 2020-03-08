## Latest changes

## 0.0.9

* Add support for PEP 561, to allow `mypy` to type check applications built with **Typer**. PR [#58](https://github.com/tiangolo/typer/pull/58).
* Upgrade deploy docs to Netlify GitHub action. PR [#57](https://github.com/tiangolo/typer/pull/57).
* Add support for Mermaid JS for visualizations. PR [#56](https://github.com/tiangolo/typer/pull/56).
* Update CI to run docs deployment in GitHub actions. PR [#50](https://github.com/tiangolo/typer/pull/50).
* Update format for internal links. PR [#38](https://github.com/tiangolo/typer/pull/38).
* Tweak external links' format. PR [#36](https://github.com/tiangolo/typer/pull/36).

## 0.0.8

* Update docs and add latest changes to MkDocs/website. PR [#33](https://github.com/tiangolo/typer/pull/33).
* Add extra tests for edge cases that don't belong in docs' examples. PR [#32](https://github.com/tiangolo/typer/pull/32).
* Add docs for CLI Parameters with [Multiple Values](https://typer.tiangolo.com/tutorial/multiple-values/). Includes tests for all the examples and bug fixes. PR [#31](https://github.com/tiangolo/typer/pull/31).
* Add docs for extra *CLI parameter* types: [CLI Parameter Types: Number](https://typer.tiangolo.com/tutorial/parameter-types/number/) and [CLI Parameter Types: Boolean CLI Options](https://typer.tiangolo.com/tutorial/parameter-types/bool/). PR [#30](https://github.com/tiangolo/typer/pull/30).
* Extend docs for Commands, add [Commands: Typer Callback](https://typer.tiangolo.com/tutorial/commands/callback/) and [Commands: One or Multiple](https://typer.tiangolo.com/tutorial/commands/one-or-multiple/). This includes tests for all the examples and bug fixes. PR [#29](https://github.com/tiangolo/typer/pull/29).
* Add docs for [SubCommands - Command Groups](https://typer.tiangolo.com/tutorial/subcommands/). This includes tests for all the examples and bug fixes. PR [#28](https://github.com/tiangolo/typer/pull/28).
* Remove unneeded code for argument handling. PR [#26](https://github.com/tiangolo/typer/pull/26).
* Add docs for [Launching Applications](https://typer.tiangolo.com/tutorial/launch/). PR [#25](https://github.com/tiangolo/typer/pull/25).
* Add docs for getting the [CLI Application Directory](https://typer.tiangolo.com/tutorial/app-dir/). PR [#24](https://github.com/tiangolo/typer/pull/24).
* Add docs for [Progress Bars](https://typer.tiangolo.com/tutorial/progressbar/). PR [#23](https://github.com/tiangolo/typer/pull/23).
* Add docs for [Asking with Interactive Prompts](). PR [#22](https://github.com/tiangolo/typer/pull/22).
* Update docs for path *CLI option*. PR [#21](https://github.com/tiangolo/typer/pull/21).
* Add colors module and docs for [Printing and Colors](https://typer.tiangolo.com/tutorial/printing/) and for [Terminating](https://typer.tiangolo.com/tutorial/terminating/), including tests. PR [#20](https://github.com/tiangolo/typer/pull/20).
* Refactor docs to make each individual page/section "bite-sized" / small. Add docs for [CLI option names](https://typer.tiangolo.com/tutorial/options/name/). Update `typer.Argument()` to remove invalid positional `param_decls`. PR [#19](https://github.com/tiangolo/typer/pull/19).

## 0.0.7

* Add docs for [*CLI parameter* types](https://typer.tiangolo.com/tutorial/parameter-types/). Includes tests and file classes refactor. PR [#17](https://github.com/tiangolo/typer/pull/17).
* Add tests for completion. PR [#15](https://github.com/tiangolo/typer/pull/15) and [#16](https://github.com/tiangolo/typer/pull/16).

## 0.0.6

* Add docs for [Commands](https://typer.tiangolo.com/tutorial/commands/). Includes a bug fix for handling default values set in `typer.Typer()` parameters. PR [#14](https://github.com/tiangolo/typer/pull/14).
* Add docs for [CLI Arguments](https://typer.tiangolo.com/tutorial/arguments/). PR [#13](https://github.com/tiangolo/typer/pull/13).
* Add docs for [CLI Options](https://typer.tiangolo.com/tutorial/options/). PR [#12](https://github.com/tiangolo/typer/pull/12).

## 0.0.5

* Clean exports from Typer. Remove unneeded components from Click and add needed `Exit` exception. PR [#11](https://github.com/tiangolo/typer/pull/11).
* Fix and document extracting help from a function's docstring [First Steps: Document your CLI app](https://typer.tiangolo.com/tutorial/first-steps/#document-your-cli-app). PR [#10](https://github.com/tiangolo/typer/pull/10).
* Update references to `--install-completion` and `--show-completion` in docs. PR [#9](https://github.com/tiangolo/typer/pull/9).
* Fix testing utilities, add tests for First Steps examples. PR [#8](https://github.com/tiangolo/typer/pull/8).
* Add auto completion options by default when [click-completion](https://github.com/click-contrib/click-completion) is installed: `--install-completion` and `--show-completion`. PR [#7](https://github.com/tiangolo/typer/pull/7).
* Update Termynal to have fixed sizes, add "fast" button, and use it in [First Steps](https://typer.tiangolo.com/tutorial/first-steps/). PR [#6](https://github.com/tiangolo/typer/pull/6).
* Add custom automatic [Termynal](https://github.com/tiangolo/termynal) for docs. PR [#5](https://github.com/tiangolo/typer/pull/5).

## 0.0.4

* Update short descriptions and assets.
* Docs rewording and fix typos. PR [#1](https://github.com/tiangolo/typer/pull/1) by [@mariacamilagl](https://github.com/mariacamilagl).

## 0.0.3

* Fix group creation without name.

## 0.0.2

* Add initial version of code, docs, etc.

## 0.0.1

* First commit. Publish to PyPI to reserve package name.
