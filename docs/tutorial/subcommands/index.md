You read before how to create a program with [Commands](../commands/index.md){.internal-link target=_blank}.

Now we'll see how to create a *CLI program* with commands that have their own subcommands. Also known as command groups.

For example, the *CLI program* `git` has a command `remote`.

But `git remote`, in turn, has its own subcommands, like `add`:

<div class="termy">

```console
// git remote alone shows the current remote repositories
$ git remote

origin

// Use -v to make it verbose and show more info
$ git remote -v

origin  git@github.com:yourusername/typer.git (fetch)
origin  git@github.com:yourusername/typer.git (push)

// git remote add takes 2 CLI arguments, a name and URL
$ git remote add upstream https://github.com/tiangolo/typer.git

// Doesn't output anything, but now you have another remote repository called upstream

// Now check again
$ git remote -v

origin  git@github.com:yourusername/typer.git (fetch)
origin  git@github.com:yourusername/typer.git (push)
upstream        https://github.com/tiangolo/typer.git (fetch)
upstream        https://github.com/tiangolo/typer.git (push)
```

</div>

In the next sections we'll see how to create subcommands like these.
