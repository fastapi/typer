# Repository Management

Here's a short description of how the Typer repository is managed and maintained.

## Owner

I, [@tiangolo](https://github.com/tiangolo), am the creator and owner of the Typer repository. 🤓

I normally give the final review to each PR before merging them. I make the final decisions on the project, I'm the [<abbr title="Benevolent Dictator For Life">BDFL</abbr>](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life). 😅

## Team

There's a team of people that help manage and maintain the project. 😎

They have different levels of permissions and [specific instructions](./management-tasks.md).

Some of the tasks they can perform include:

* Adding labels to PRs.
* Editing PR titles.
* Adding commits on top of PRs to tweak them.
* Mark answers in GitHub Discussions questions, etc.
* Merge some specific types of PRs.

Joining the team is by invitation only, and I could update or remove permissions, instructions, or membership.

### Team Members

This is the current list of team members. 😎

<div class="user-list user-list-center">
{% for user in members["members"] %}

<div class="user"><a href="https://github.com/{{ user.login }}"><div class="avatar-wrapper"><img src="https://github.com/{{ user.login }}.png"/></div><div class="title">@{{ user.login }}</div></a></div>
{% endfor %}

</div>

Additional to them, there's a large community of people helping each other and getting involved in the projects in different ways.

## External Contributions

External contributions are very welcome and appreciated, including answering questions, submitting PRs, etc. 🙇‍♂️

There are many ways to [help maintain Typer](./help-typer.md).
