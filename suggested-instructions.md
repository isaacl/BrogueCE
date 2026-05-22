# Suggested Instructions

## General Rules (all languages)

### File System

- **No check-then-act**: Never check filesystem state and then assume it hasn't changed. Two system calls (a check then an operation depending on the check) are a race condition. Use atomic operations (`open(..., "xb")`, rename, etc.) or handle the error from the operation itself.
- **No intermediate path checks**: Check the final target, not parent directories. Missing parents produce clear OS errors.
- **Prefer APIs that batch information**: Use calls that return stats alongside listings (e.g. `os.scandir()`) instead of listing then stat-ing individually. Let the API docs guide which call is appropriate.

### External Commands & Safety

- **Never use untrusted text in system calls or file paths**: Output from commands like `brew --prefix` must be validated (e.g. is an absolute path, contains no unexpected characters) before being used in filesystem operations or passed to further commands. An unexpected value could overwrite critical files.
- **Do not silence stderr**: Never redirect stderr to DEVNULL unless you have confirmed the program emits meaningless noise on stderr. Stderr from failing commands is debugging information.
- **Check API of any call**: Look up actual defaults, return types, error behavior, and context manager protocols before using any function or command. Do not assume—read docs or source.

### Error Handling

- **No safety nets for invalid input**: If arguments are invalid, raise/return an error. Never silently clamp, adjust, or guess.
- **No fluff around fatal errors**: Do not wrap exceptions in nicer text that obscures the traceback. Let exceptions propagate with their original context. A clear stack trace is more useful than a pretty message.
- **Use `add_note` over squelching**: When catching an exception to add context, use `e.add_note(...)` and re-raise rather than replacing the exception with a string or swallowing it.
- **Fail fast**: If a required tool or path isn't available, fail immediately with a clear error. Do not fall back to guessing.

### Code Style

- **Truthiness over `is None`**: Use `if not x` / `if x` when truthiness is sufficient. Only use `is None` when distinguishing `None` from other falsy values matters.
- **Inline single-use functions**: If a function is compact, self-explanatory, and only called once, inline it.
- **Inline self-explanatory constants**: If a constant is used once and obvious from context, use the literal.
- **No unused imports**: Only import what you use.
- **Tuple unpack over indexing**: Use `base, _ = os.path.splitext(...)` instead of `os.path.splitext(...)[0]`. Prefer named decomposition.
- **Don't annotate types that can be inferred**: Only add type annotations where the type is not obvious from the right-hand side. Redundant annotations are noise.

### Documentation Access

- If a request is for a patch (not a standalone script) and you cannot access project documentation (wiki, architecture docs, etc.), the proposed PR title must start with "NO DOCS" and the description must include details about what documentation was inaccessible.
- For standalone scripts, it should still be obvious from the PR description if documentation was unavailable but it need not be in the title.

### Working on PRs

- **Merge main branch**: At the start of each session, check if there are new commits on the main branch and merge them into your PR branch unless it is clearly non-productive. If you skip the merge, note that you skipped it and why.
- **Check available resources**: When you cannot find or understand a referenced document, check: (1) the main branch for new pushes, (2) submodules (`git submodule update --init`), (3) the GitHub issue tracker via MCP tools if available. Do not assume content is missing without exhausting these avenues.
- **Track unaddressed requests**: If a reviewer asks for something and you do not do it in the current commit, explicitly state what was not done and why. Never silently drop a request.

## Python

### Scripts (single-file, has shebang)

- **Shebang**: `#!/usr/bin/env python`
- **Entry point**: Last line must be `exit(main(sys.argv[1:]))`. No `sys.exit` or `exit` anywhere else.
- **`main(argv)` signature**: Accept `argv: list[str]` as parameter. Return `int` (exit code) or `str` (error message printed to stderr, exits 1).
- **Type annotations**: Add types to function signatures and locals where the type is not obvious from context. Use a typed `argparse.Namespace` subclass for parsed args.
- **No pathlib**: Use `os.path` exclusively.
- **No Windows support**: Never add Windows-specific code unless explicitly requested.
- **Logging over print**: Use `logging.info`, `logging.debug`, etc. (module-level `logging`). Set up `logging.basicConfig` with a `--verbose`/`-v` flag.
- **Argparse**: Keep help strings concise. Don't repeat defaults in help text. Don't specify API defaults that match the built-in (e.g. `default=None`, `type=str`).
- **OS detection**: Use `os.uname()` for platform information. Avoid the `platform` module for simple detection.

### Projects (multi-file, no shebang)

- Entry point defined in `pyproject.toml` or `setup.py` console_scripts.
- Use a logger instance (`logger = logging.getLogger(__name__)`) rather than module-level `logging` calls.
- `pathlib` is acceptable in projects where it improves readability.
- Type annotations required on all public interfaces.

### Common (scripts and projects)

- **Function extraction threshold**: Extract when a function has a clear name, is non-trivial (>5-10 lines), and/or is called more than once.
- **Tests required**: Every script/module must have at least a smoke test (invocable, doesn't crash on `--help` and basic inputs). Create a test script alongside the tool.
- **No accommodation for weird setups**: If discovery fails, error out clearly.

## Open Questions

| Question | Resolution |
|----------|-----------|
| Should `find_data_dir` be inlined into main? | Kept as a function: multiple early-return points and raises make inlining harder to read. |
| Should error from main be an exception or return string? | Return string per convention. Sub-function exceptions propagate naturally with `add_note`. |
| `exit()` vs `sys.exit()`? | `exit(main(sys.argv[1:]))` per convention. `exit` is a builtin that prints strings to stderr and exits 1. |
| Wiki/submodule access? | Submodule works after `git submodule update --init`. Must merge main branch first if submodule was added there. |
