#!/usr/bin/env python
"""Convert a Brogue recording (.broguerec) into a save file (.broguesave)
rolled back a number of turns so the game can be resumed before death.

The recording and save formats share an identical binary layout. The only
difference is that a save file has its turn counter (header offset 24-27,
4-byte big-endian uint) set to the turn at which play should resume. On
load, Brogue replays the event stream up to that turn and then switches
to live play.

Usage examples:
    # Use LastRecording.broguerec in default data dir, roll back 5 turns
    python tools/recover_save.py

    # Roll back 10 turns from a specific recording
    python tools/recover_save.py --turns 10 --recording /path/to/game.broguerec

    # Specify data directory explicitly
    python tools/recover_save.py --data-dir /opt/homebrew/var/brogue
"""

import argparse
import logging
import os
import struct
import subprocess
import sys


class Args(argparse.Namespace):
    turns: int
    recording: str | None
    data_dir: str | None
    output: str | None
    verbose: bool


def find_data_dir() -> str:
    """Locate the Brogue data directory via brew --prefix."""
    try:
        prefix = subprocess.check_output(["brew", "--prefix"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError("brew --prefix failed; specify --data-dir or --recording")
    if not os.path.isabs(prefix):
        raise RuntimeError(f"brew --prefix returned non-absolute path: {prefix!r}")
    path = os.path.join(prefix, "var", "brogue")
    if not os.path.isdir(path):
        raise RuntimeError(f"Brogue data directory not found: {path}")
    return path


def main(argv: list[str]) -> int | str:
    parser = argparse.ArgumentParser(
        description="Convert a Brogue recording into a save file rolled back N turns.",
        epilog=(
            "If no recording is specified, LastRecording.broguerec in the "
            "data directory is used. The data directory is found via brew --prefix."
        ),
    )
    parser.add_argument(
        "-t", "--turns", type=int, default=5,
        help="Number of turns to roll back.",
    )
    parser.add_argument(
        "-r", "--recording",
        help="Path to the .broguerec file to convert.",
    )
    parser.add_argument(
        "-d", "--data-dir",
        help="Brogue data/saves directory.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path for the .broguesave file.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose logging.",
    )
    args = parser.parse_args(argv, namespace=Args())

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Resolve recording path
    recording_path = args.recording
    if not recording_path:
        out_dir = args.data_dir or find_data_dir()
        recording_path = os.path.join(out_dir, "LastRecording.broguerec")
    else:
        out_dir = args.data_dir

    # Read the file
    with open(recording_path, "rb") as f:
        data = bytearray(f.read())

    original_turns, = struct.unpack_from(">I", data, 24)

    if not original_turns:
        return "Recording has 0 turns; nothing to roll back."

    if args.turns >= original_turns:
        return f"rollback of {args.turns} turns exceeds game ({original_turns} turns)"

    new_turns = original_turns - args.turns

    struct.pack_into(">I", data, 24, new_turns)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base, _ = os.path.splitext(os.path.basename(recording_path))
        filename = f"{base}_recovered_turn{new_turns}.broguesave"
        if out_dir:
            output_path = os.path.join(out_dir, filename)
        else:
            output_path = os.path.join(os.path.dirname(os.path.abspath(recording_path)), filename)

    # Write output; fail if file already exists to avoid accidental overwrites
    try:
        with open(output_path, "xb") as f:
            f.write(data)
    except FileExistsError as e:
        e.add_note(f"Output file already exists: {output_path}")
        raise

    logging.debug("Turn count: %d -> %d (rolled back %d)", original_turns, new_turns, args.turns)
    if not args.output:
        logging.info("Save written: %s", output_path)


if __name__ == "__main__":
    exit(main(sys.argv[1:]))
