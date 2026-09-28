# Development - Contributing

First, you might want to see the basic ways to [help Typer and get help](https://typer.tiangolo.com/help-typer/).

## Developing

To contribute code to the project, please follow the guidelines in [tiangolo.com - Contributing](https://tiangolo.com/open-source/contributing/).

## Completion

To try and test the completion for different shells and check that they are working you can use a Docker container.

There's a `Dockerfile` and a Docker Compose file `compose.yaml` at `./scripts/docker/`.

It has installed `bash`, `zsh`, `fish`, and `pwsh` (PowerShell for Linux).

It also has installed `nano` and `vim`, so that you can check the modified configuration files for the shells (for example `.bashrc`, `.zshrc`, etc).

It also has `uv` installed, so you can install the dependencies and the project quickly.

The Docker Compose file mounts the main directory as `/code` inside the container, so you can change things and try them out.

Go to the `./scripts/docker/` directory:

```console
$ cd scripts/docker/
```

Then run an interactive session with `bash` inside the container:

```console
$ docker compose run typer bash

root@79c4b9b70cbe:/code#
```

Then inside the container, you can install `typer` with:

```console
$ uv pip install -r requirements.txt
```

Then, you can start the shell you want to use, the one where you want to try out completion:

* `bash`
* `fish`
* `pwsh`
* `zsh`

For example:

```console
$ zsh
```

Then install `typer` completion:

```console
$ typer --install-completion
```

/// note

In `pwsh` you will probably get a warning of:

```plaintext
Set-ExecutionPolicy: Operation is not supported on this platform.
```

this is because that configuration is only available in Windows (and needed there), not in PowerShell for Linux.

///

For completion to take effect, you need to restart the shell. So, exit the current shell:

```console
$ exit
```

and start a new shell (for the same shell you installed completion in) again. For example:

```console
$ zsh
```

Now you could create a demo file on the same Typer directory in your editor, for example `demo.py`:

```python
import typer

app = typer.Typer()


@app.command()
def hello():
    print("Hello")


@app.command()
def goodbye():
    print("Goodbye")


if __name__ == "__main__":
    app()
```

Because the directory is mounted as a volume, you will be able to access the file from inside the container.

So, you can try running it with the `typer` command, that will use the installed shell completion:

```console
$ typer demo.py <TAB>
```

And you should see the completion working:

```console
run    -- Run the provided Typer app.
utils  -- Extra utility commands for Typer apps.
```

And the same for the commands in your `demo.py` file:

```console
$ typer demo.py run <TAB>

hello    goodbye
```

You can also check the configuration file using `nano` or `vim`, for example:

```bash
nano ~/.zshrc
```

It will show some content like:

```bash
fpath+=~/.zfunc; autoload -Uz compinit; compinit


zstyle ':completion:*' menu select
```

If you exit from the container, you can start a new one, you will probably have to install the packages again and install completion again.

Using this process, you can test all the shells, with their completions, being able to start from scratch quickly in a fresh container, and verifying that everything works as expected.
