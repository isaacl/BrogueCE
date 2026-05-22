# Suggested Instructions for Python Scripts

## Firm Rules

- **Entry point**: The last line of any script must be `exit(main(sys.argv[1:]))`. `sys.exit` / `exit` is banned anywhere else in the file.
- **Error handling in main**: Return a string (displayed as error) or integer exit code. In sub-functions, raise an exception to signal failure. Never print warnings or error text directly.
- **No pathlib**: Use `os.path` exclusively for all path operations.
- **No Windows support**: Never add Windows-specific code unless explicitly requested.
- **No `print` for status**: Use `logging.info`, `logging.debug`, etc. (module-level `logging`, not a logger instance in single-file scripts). Set up `logging.basicConfig` with a `--verbose` flag via argparse.
- **Truthiness over `is None`**: Use `if not x` / `if x` when truthiness is sufficient. Only use `is None` when distinguishing `None` from other falsy values (0, empty string) matters.
- **No defensive filesystem checks**: Do not check if a path exists before reading/writing. Use try/except. For writes, use `open(..., "xb")` or `"x"` mode to atomically fail if the file exists. Checking-then-acting is a race condition and more verbose.
- **No intermediate path checks**: Check the final target path, not parent directories. If a parent doesn't exist the operation will fail with a clear OS error.
- **Do not stat files individually**: When finding files in a directory, use `os.scandir()` which returns stats with the listing. Never use `glob`. List all entries and filter in code.
- **Do not silence stderr**: Never redirect stderr to DEVNULL unless you have confirmed the program emits meaningless noise on stderr.
- **Validate external command output**: If shelling out to a command (e.g. `brew --prefix`), verify the output is sane (e.g. is an absolute path) before using it in filesystem operations.
- **No safety nets for invalid input**: If arguments are invalid (file doesn't exist, rollback exceeds turns), raise an exception or return an error. Never silently clamp or adjust.
- **Inline single-use functions**: If a function is compact, self-explanatory, and only called once, inline it. Do not create wrappers around one-liners like `struct.unpack_from`.
- **Inline self-explanatory constants**: If a constant (like `".broguerec"`) is only used once and its meaning is obvious from context, use the literal. Constants that are non-obvious but used in only one function should be defined immediately above that function, not at module top.
- **Do not specify API defaults**: If an argparse argument's `default` is `None` (the built-in default), do not write `default=None`. If `type` is `str` (the default for optional args), do not write `type=str`. Always look up actual defaults before writing code.
- **No accommodation for weird setups**: If `brew --prefix` fails, do not fall back to hardcoded paths. If the expected tool/path isn't available, fail immediately with a clear error.
- **Argparse**: Include `--verbose` (or `-v`) flag for log level. Keep help strings concise. Don't repeat the default in help text unless it's non-obvious.
- **`main(argv)` signature**: Accept argv as a parameter (enables testing). Parse args from this parameter, not from implicit sys.argv.
- **Tests required**: Every script must have tests that were run before review. At minimum, test with sample parameters that exercise the main codepath and error cases.

## Proposed / Under Consideration

- **sys.platform checks**: Use `sys.platform == "darwin"` for macOS, `sys.platform.startswith("linux")` for Linux. Avoid the `platform` module for simple OS detection.
- **brew is cross-platform**: `brew` can exist on Linux (Linuxbrew). Don't gate `brew --prefix` behind a macOS check unless there's a reason to.
- **Logging format**: `"%(levelname)s: %(message)s"` is a reasonable default for scripts. Consider `"%(message)s"` if the level prefix is noisy for INFO-only output.
- **File handling pattern**: Prefer `with open(...) as f` over standalone read/write helpers. This is also naturally compatible with the try/except-on-open style.
- **Function extraction threshold**: Extract a function when it has a clear name, is non-trivial (>5-10 lines), and/or is called more than once. Single-use 3-line helpers should be inline.
- **Script-level constants**: Only promote a value to a module-level constant if it is: (a) used in multiple places, OR (b) non-obvious and benefits from a name for readability. Otherwise, inline it.
- **Submodule / wiki access**: Copilot agents currently cannot access GitHub wiki pages. If instructions reference a wiki or architecture page that can't be accessed, note this explicitly as a caveat in the response.
- **Return type from main**: `return 0` for success, `return "error message string"` for failure. The `exit()` builtin handles both (prints string to stderr and exits 1, or exits with the int code).
- **Shebang**: Always `#!/usr/bin/env python3`.
- **No unused imports**: Only import what you use. Don't import modules speculatively.

## Open Questions & Resolutions

| Question | Resolution |
|----------|-----------|
| Should `find_data_dir` be inlined into main? | Kept as a function because it has multiple early-return points and raises; inlining would make main harder to read (~10 lines of logic). |
| Should `find_most_recent_recording` be inlined? | Kept as a function because it encapsulates a scan+filter loop that would clutter main. It's also a plausible candidate for reuse across future scripts. |
| Should error from main be an exception or return string? | Return string per the stated convention. Exceptions from sub-functions propagate naturally since we don't catch them in main. |
| `exit()` vs `sys.exit()`? | Instructions say `exit(main(sys.argv[1:]))` specifically. `exit` is a builtin that works the same as `sys.exit` for our purposes (prints string to stderr, exits 1). |
| What about the wiki submodule mentioned in instructions? | Could not find a wiki submodule in the repo. Noted as a caveat: if the user pushed it after this session's clone, it won't be visible. |
| Should `brew --prefix` stderr be suppressed? | No, per instruction. brew doesn't emit meaningless stderr; if it errors, the stderr is useful. |
| rollback-past-turn-1 behavior: clamp or error? | Error per "do not code safeties" instruction. If user requests more turns than exist, that's an invalid input. |
