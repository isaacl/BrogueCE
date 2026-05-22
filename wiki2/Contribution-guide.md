Thanks for your interest in helping to develop Brogue CE.

We have a Discord server for contributors; feel free to join it:
<https://discord.gg/8pxE4j8>

There are some ports of CE. They adopt all our changes, but you can contribute to port-specific parts at their repos:

- Web Brogue: <https://github.com/flend/web-brogue>
- iPad: <https://github.com/btaylor84/iBrogueCE>

For general help on using GitHub: <https://docs.github.com/>

## How you can help

- **Test** the latest changes, and let us know what you
  think and report any bugs you run into. See [[Playing dev versions]].

- **Fix bugs.** See issues labelled "bug". (Also see the "good first issue" label for suggested starter fixes.)

- **Implement features.** Tickets with the "enhancement" label are considered to be welcome additions and just need someone to pick them up.

- **Add detail to ideas and tickets.** Unlabeled but open tickets just need some
  more attention or discussion to decide what they really mean and whether we
  want to try them. Turning a vague feature idea into a more detailed
  description can be useful to figure out edge cases and also helps whoever
  might implement it.

- **Improve the tiles** (`bin/assets/tiles.png`) or make new alternative tile sets.

## Pull request guide

### Base branch

PRs should be based on:

* "master" for gameplay changes or anything which breaks replays, for the next 1.Y version
* "release" for anything which doesn't break replays, for the next 1.y.Z version

### Commits

I squash most PRs to one commit, so you can work how you like on your branch.

If you specifically want your PR to be merged as multiple commits, I find a clear Git history very beneficial to work with, so I care quite a bit
about how they are presented.

Please read my [tips for using Git effectively][Git guidance], which can be
considered guidelines for contributing to this project.

[Git guidance]: https://tmewett.com/git-guidance/

### Change files

When making user-facing changes, please add a non-technical description of each
change to a .md file in `changes/`. These files are collated to
create the release notes.

If the change is from one commit, include this file in it. For a branch of
multiple commits, add it in a separate commit.

## Code style

New code should follow these guidelines:

- Use 4 spaces of indentation.
- Be consistent with formatting (pay attention to whitespace between brackets,
  commas, etc.) and try to follow how existing code looks.
- Declare functions and variables local to a file as `static`.
- Use `int` for generic integer declarations, not `short` like a lot of existing code does.
- Do not pre-declare all variables at the top of functions, like some existing code does; declare them naturally, where needed.
- Use braces for control structures on multiple lines:

  ```c
  // no
  if (cond)
      action();

  // yes
  if (cond) {
      action();
  }

  // acceptable
  if (cond) action();
  ```

- When writing bracketed lists over multiple lines, wrap it naturally and don't
  align to the open bracket (this includes declarations):

  ```c
  // yes
  some_function(
      a, b,
      c,
      d
  );

  // no
  some_function(a, b,
                c,
                d);
  ```

- When writing multi-line if/while conditions, use at least the same indentation
  as the body. It can be clearer to over-indent to separate it

  ```c
  // same indent is ok, but...
  while ((A && B)
      || C) {
      ...
  }

  // over-indent can be clearer
  while ((A && B)
          || C) {
      ...
  }

  // a gap works too
  while ((A && B)
      || C) {

      ...
  }
  ```
