# Vendored Click

/// note

This is historical information, if you are just learning Typer from scratch, you don't need to read it. ☕️

///

Typer used to depend on [Click](https://click.palletsprojects.com/), a popular tool for building CLIs in Python, as an external dependency.

Since version 0.26.0, Typer has vendored Click (included Click's source code internally, instead of installing it as a third party package) and has unified the code interactions between Typer and the embedded Click source code for easier maintainability in the future.

Note that some Click functionality will not be available anymore in the future, as we continue to improve and extend Typer's codebase.

## Breaking Changes

Typer used to support extracting the internal Click app from a Typer app to use and modify it with any Click functionality. For example, to add Click-specific plug-ins.

The same way, it supported adding Click-specific types to override the default Typer ones.

Using Click directly was an edge case feature that was not commonly used, and it is no longer supported. If your app depended specifically on this, you will need to either migrate it to use plain Typer, or migrate it to use Click directly instead of Typer.

## Codebase Compatibility Improvements

Because Typer used to depend on Click, any new features or changes in newer Click versions could break compatibility in Typer.

The Click team has always been very helpful and supportive with Typer. But still, this dependency interaction would cause extra effort and burden for both the Typer team and the Click team.

Now that Typer continues evolving, starting from a fixed copy of Click's source code, any changes in Click's codebase will not affect Typer.

The Typer team will not need to make sure there are workarounds for changes in new versions of Click, and the Click team will not need to consider additional edge cases caused by Typer.

## Compatibility Improvements for Your Apps

The fact that Typer depended on Click caused an additional ongoing issue that could happen from time to time to user projects.

Many packages come with a CLI, some of them could use Click, some could use Typer.

Some of these packages could require a recent version of Click that Typer still didn't support, but as all these package dependencies would belong to the same project, there would be conflicts.

In these cases, the package that depended on the newer version of Click would require installing it, but the other package that used Typer would break. Or if there were version pins, some combinations of packages would not be installable together.

Across different versions of Click through time, there were many changes needed in Typer to make it all compatible with multiple versions of Click at the same time.

Now that Typer and Click are decoupled, a package could depend on a newer version of Click, while another package that uses Typer would continue working as normally, as that Typer version would bundle anything necessary from Click's source code to work.

## Future Improvements

Both the Click team and the Typer team have future improvements planned, not having to coordinate with each other for compatibility will simplify the work of both teams.

In some cases feature ideas could overlap, and could have caused incompatibilities. Now this won't be a problem as each team can focus on each project independently.

## Typer Changes

After vendoring Click, Typer will reduce, simplify and refactor parts of the vendored Click code that are not necessary for Typer, or that could be done in a different way to facilitate future improvements in Typer.

Then Typer will gradually introduce new features and improvements that have been planned for a while but were too difficult to implement before this.

## User Focus

These decisions are all carefully planned and based on real world use cases extracted from the official Typer developer survey, including the tradeoff between the potential breaking changes for some use cases and the planned future features and improvements that will be enabled.

## Thank You Click

Click has been the foundation building block of Typer and most CLI's in Python (through Typer or directly with Click).

We wouldn't be here without Click, and we are very grateful for all the work that the Click team has done.

Thank you Click! 🙇
