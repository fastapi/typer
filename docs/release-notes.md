## Latest Changes


## 0.5.0

### Features

* ✨ Add pretty error tracebacks for user errors and support for Rich. PR [#412](https://github.com/tiangolo/typer/pull/412) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏ Fix typo, "ASCII codes" to "ANSI escape sequences". PR [#308](https://github.com/tiangolo/typer/pull/308) by [@septatrix](https://github.com/septatrix).

## 0.4.2

### Fixes

* 🐛 Fix type conversion for `List` and `Tuple` and their internal types. PR [#143](https://github.com/tiangolo/typer/pull/143) by [@hellowhistler](https://github.com/hellowhistler).
* 🐛 Fix `context_settings` for a Typer app with a single command. PR [#210](https://github.com/tiangolo/typer/pull/210) by [@daddycocoaman](https://github.com/daddycocoaman).

### Docs

* 📝 Clarify testing documentation about checking `stderr`. PR [#335](https://github.com/tiangolo/typer/pull/335) by [@cgabard](https://github.com/cgabard).
* ✏ Fix typo in docs for CLI Option autocompletion. PR [#288](https://github.com/tiangolo/typer/pull/288) by [@graue70](https://github.com/graue70).
* 🎨 Fix header format for "Standard Input" in `docs/tutorial/printing.md`. PR [#386](https://github.com/tiangolo/typer/pull/386) by [@briancohan](https://github.com/briancohan).
* ✏ Fix typo in `docs/tutorial/terminating.md`. PR [#382](https://github.com/tiangolo/typer/pull/382) by [@kianmeng](https://github.com/kianmeng).
* ✏ Fix syntax typo in `docs/tutorial/package.md`. PR [#333](https://github.com/tiangolo/typer/pull/333) by [@ryanstreur](https://github.com/ryanstreur).
* ✏ Fix typo, duplicated word in `docs/tutorial/options/required.md`.. PR [#316](https://github.com/tiangolo/typer/pull/316) by [@michaelriri](https://github.com/michaelriri).
* ✏ Fix minor typo in `index.md`. PR [#274](https://github.com/tiangolo/typer/pull/274) by [@RmStorm](https://github.com/RmStorm).
* ✏ Fix double "and" typo in first-steps tutorial. PR [#225](https://github.com/tiangolo/typer/pull/225) by [@softwarebloat](https://github.com/softwarebloat).
* 🎨 Fix format in docs explaining `datetime` parameter type. PR [#220](https://github.com/tiangolo/typer/pull/220) by [@DiegoPiloni](https://github.com/DiegoPiloni).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#404](https://github.com/tiangolo/typer/pull/404) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 👷 Fix Material for MkDocs install in CI. PR [#395](https://github.com/tiangolo/typer/pull/395) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add pre-commit CI config. PR [#394](https://github.com/tiangolo/typer/pull/394) by [@tiangolo](https://github.com/tiangolo).
* 👷 Clear MkDocs Insiders cache. PR [#393](https://github.com/tiangolo/typer/pull/393) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add pre-commit config and formatting. PR [#392](https://github.com/tiangolo/typer/pull/392) by [@tiangolo](https://github.com/tiangolo).
* 👷 Disable installing MkDocs Insiders in forks. PR [#391](https://github.com/tiangolo/typer/pull/391) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade Codecov GitHub Action. PR [#383](https://github.com/tiangolo/typer/pull/383) by [@tiangolo](https://github.com/tiangolo).

## 0.4.1

### Fixes

* 🐛 Fix import of `get_terminal_size` for Click 8.1.0 support and upgrade Black to fix CI. PR [#380](https://github.com/tiangolo/typer/pull/380) by [@tiangolo](https://github.com/tiangolo) based on original PR [#375](https://github.com/tiangolo/typer/pull/375) by [@madkinsz](https://github.com/madkinsz).

### Internal

* 📝 Add Jina's QA Bot to the docs to help people that want to ask quick questions. PR [#368](https://github.com/tiangolo/typer/pull/368) by [@tiangolo](https://github.com/tiangolo).
* 💚 Only test on push when on master, avoid duplicate CI runs from PRs. PR [#358](https://github.com/tiangolo/typer/pull/358) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add support for previewing docs in PRs from forks and enable MkDocs Insiders. PR [#357](https://github.com/tiangolo/typer/pull/357) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade MkDocs Material, MDX-Include, and MkDocs structure. PR [#356](https://github.com/tiangolo/typer/pull/356) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update publish GitHub action. PR [#325](https://github.com/tiangolo/typer/pull/325) by [@tiangolo](https://github.com/tiangolo).

## 0.4.0

### Features

* ✨ Add support for Click 8 while keeping compatibility with Click 7. PR [#317](https://github.com/tiangolo/typer/pull/317) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 📝 Add Security policy. PR [#324](https://github.com/tiangolo/typer/pull/324) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add updated issue templates. PR [#323](https://github.com/tiangolo/typer/pull/323) by [@tiangolo](https://github.com/tiangolo).
* 👷 Enable tests for Python 3.9. PR [#322](https://github.com/tiangolo/typer/pull/322) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action Latest Changes. PR [#321](https://github.com/tiangolo/typer/pull/321) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update docs CI name. PR [#320](https://github.com/tiangolo/typer/pull/320) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add sponsors docs and badge. PR [#319](https://github.com/tiangolo/typer/pull/319) by [@tiangolo](https://github.com/tiangolo).

## 0.3.2

### Features

* Add support for `mypy --strict`. Original PR [#147](https://github.com/tiangolo/typer/pull/147) by [@victorphoenix3](https://github.com/victorphoenix3).

### Docs

* Update docs with new `--help` showing default values. PR [#135](https://github.com/tiangolo/typer/pull/135) by [@victorphoenix3](https://github.com/victorphoenix3).
* Add `Optional` to docs for *CLI Arguments and Options* with a default of `None`. PR [#131](https://github.com/tiangolo/typer/pull/131) by [@rkbeatss](https://github.com/rkbeatss).
* Add valid date formats to docs. PR [#122](https://github.com/tiangolo/typer/pull/122) by [@IamCathal](https://github.com/IamCathal).

### Internal

* Report coverage in XML to support GitHub Actions. PR [#146](https://github.com/tiangolo/typer/pull/146).
* Update badges and remove Travis, now that GitHub Actions is the main CI. PR [#145](https://github.com/tiangolo/typer/pull/145).

## 0.3.1

* Add GitHub Actions, move from Travis. PR [#144](https://github.com/tiangolo/typer/pull/144).
* Pin dependencies. PR [#138](https://github.com/tiangolo/typer/pull/138).
* Add Dependabot. PR [#136](https://github.com/tiangolo/typer/pull/136).
* Upgrade Isort to version 5.x.x. PR [#137](https://github.com/tiangolo/typer/pull/137).

## 0.3.0

* Add support for `help` parameter in *CLI arguments*:
    * As `help` in *CLI arguments* is not supported by Click, there are two new internal classes (Click sub-classes) to support it:
        * `typer.core.TyperArgument`
        * `typer.core.TyperCommand`
    * This includes a new auto-generated help text section `Arguments` for *CLI arguments*, showing defaults, required arguments, etc.
    * It's also possible to disable it and keep the previous behavior, not showing automatic help for *CLI arguments* (Click's default) using the `hidden` parameter.
    * Now `show_default` is `True` by default.
    * And now `show_envvar` is `True` by default.
    * So, default values and env vars are shown in the help text by default, without having to manually enable them, for both *CLI arguments* and *CLI options*.
    * New docs:
        * [CLI Arguments Intro](https://typer.tiangolo.com/tutorial/arguments/).
        * [Optional CLI Arguments](https://typer.tiangolo.com/tutorial/arguments/optional/).
        * [CLI Arguments with Default](https://typer.tiangolo.com/tutorial/arguments/default/).
        * [CLI Arguments with Help](https://typer.tiangolo.com/tutorial/arguments/help/).
        * [CLI Arguments with Environment Variables](https://typer.tiangolo.com/tutorial/arguments/envvar/).
        * [CLI Arguments: Other uses](https://typer.tiangolo.com/tutorial/arguments/other-uses/).
        * [CLI arguments with tuples](https://typer.tiangolo.com/tutorial/multiple-values/arguments-with-multiple-values/#cli-arguments-with-tuples).
    * Lot's of tests for all the new examples in the new docs, keeping coverage at 100%.
    * PR [#123](https://github.com/tiangolo/typer/pull/123).
* Add docs for calling packages with `python -m some_package` using `__main__.py`: [Building a Package: Support `python -m`](https://typer.tiangolo.com/tutorial/package/#support-python-m-optional). PR [#121](https://github.com/tiangolo/typer/pull/121).
* Add support for `*args` and `**kwargs` when calling the Typer app, just like in Click. PR [#120](https://github.com/tiangolo/typer/pull/120) by [@teymour-aldridge](https://github.com/teymour-aldridge).
* Fix typos in README and main docs [#103](https://github.com/tiangolo/typer/pull/103) by [@mrcartoonster](https://github.com/mrcartoonster).
* Fix typo in docs. PR [#98](https://github.com/tiangolo/typer/pull/98) by [@mrcartoonster](https://github.com/mrcartoonster).
* Fix typos and rewording in docs. PR [#97](https://github.com/tiangolo/typer/pull/97) by [@mrcartoonster](https://github.com/mrcartoonster).
* Update GitHub Action issue-manager. PR [#114](https://github.com/tiangolo/typer/pull/114).

## 0.2.1

* Add support for forward references (types declared inside of strings). PR [#93](https://github.com/tiangolo/typer/pull/93).

## 0.2.0

* Add support for completion for commands/programs not available on startup.
    * This allows installing a Typer program/script in a virtual environment and still have completion globally installed.
    * PR [#92](https://github.com/tiangolo/typer/pull/92).
* Add note about `typer.echo()` and `print()` for colors in Windows. PR [#89](https://github.com/tiangolo/typer/pull/89).
* Upgrade Mkdocs-Material version, update contributing guide style. PR [#90](https://github.com/tiangolo/typer/pull/90).

## 0.1.1

* Fix completion evaluation for Bash and Zsh when the program is not installed/found. PR [#83](https://github.com/tiangolo/typer/pull/83).
* Fix completion script for Fish. PR [#82](https://github.com/tiangolo/typer/pull/82).
* Fix shell installation for Bash to `~/.bashrc` and update Windows development docs. PR [#81](https://github.com/tiangolo/typer/pull/81).
* Update coverage badge. PR [#78](https://github.com/tiangolo/typer/pull/78).

## 0.1.0

* Fix coverage instructions. PR [#72](https://github.com/tiangolo/typer/pull/72).
* Add docs for [Building a Package](https://typer.tiangolo.com/tutorial/package/). PR [#71](https://github.com/tiangolo/typer/pull/71).
* Add docs for [Using Click (with Typer)](https://typer.tiangolo.com/tutorial/using-click/). PR [#70](https://github.com/tiangolo/typer/pull/70).
* Add support for type-based callbacks and autocompletion functions, extra tests and docs:
    * Extra tests, raising coverage to 100%.
    * New docs: [Printing and Colors: "Standard Output" and "Standard Error"](https://typer.tiangolo.com/tutorial/printing/#standard-output-and-standard-error).
    * New docs: [Password CLI Option and Confirmation Prompt](https://typer.tiangolo.com/tutorial/options/password/).
    * Support for callbacks based on type annotations. New docs: [CLI Option Callback and Context](https://typer.tiangolo.com/tutorial/options/callback-and-context/).
    * New docs: [Version CLI Option, is_eager](https://typer.tiangolo.com/tutorial/options/version/).
    * Support for autocompletion functions based on type annotations. New docs: [CLI Option autocompletion](https://typer.tiangolo.com/tutorial/options/autocompletion/).
    * New docs: [Commands: Using the Context](https://typer.tiangolo.com/tutorial/commands/context/).
    * New docs: [Testing](https://typer.tiangolo.com/tutorial/testing/).
    * PR [#68](https://github.com/tiangolo/typer/pull/68).
* Fix Zsh completion install script. PR [#69](https://github.com/tiangolo/typer/pull/69).
* Fix typo in progressbar example. PR [#63](https://github.com/tiangolo/typer/pull/63) by [@ValentinCalomme](https://github.com/ValentinCalomme).

## 0.0.11

* Re-implement completion system:
    * Remove optional dependency `click-completion` (with its sub-dependencies, like Jinja).
    * Add optional dependency `shellingham` to auto detect shell to install (it was used by `click-completion`).
    * Completion now doesn't require a third party library.
        * If `shellingham` is not installed/added as a dependency, `--install-completion` and `--show-completion` take a value with the name of the shell.
    * Fix support for user provided completion in *CLI Parameters*.
    * Fix completion for files in Bash, Zsh, and Fish.
    * Add support for modern versions of PowerShell, 5, 6, and 7 (e.g. in Windows 10).
    * Add support for `pwsh` (PowerShell Core).
        * PowerShell support includes help strings for commands and *CLI Parameters*.
    * Several bug fixes.
    * Tests for the completion logic/code.
    * Tested in all the shells in Linux and Windows.
    * PR [#66](https://github.com/tiangolo/typer/pull/66).
* Fix format in docs with highlighted lines. PR [#65](https://github.com/tiangolo/typer/pull/65).
* Add docs about [Typer CLI - completion for small scripts](https://typer.tiangolo.com/typer-cli/). PR [#64](https://github.com/tiangolo/typer/pull/64).
* Add docs about [Alternatives, Inspiration and Comparisons](https://typer.tiangolo.com/alternatives/). PR [#62](https://github.com/tiangolo/typer/pull/62).
* Add [Development - Contributing Guide](https://typer.tiangolo.com/contributing/). PR [#61](https://github.com/tiangolo/typer/pull/61).

## 0.0.10

* Add support for Click version 7.1.1. PR [#60](https://github.com/tiangolo/typer/pull/60).

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
