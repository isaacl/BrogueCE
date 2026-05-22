#!/usr/bin/env python3
"""Convert a Brogue recording (.broguerec) into a save file (.broguesave)
rolled back a number of turns so the game can be resumed before death.

The recording and save formats share an identical binary layout. The only
difference is that a save file has its turn counter (header offset 24-27,
4-byte big-endian uint) set to the turn at which play should resume. On
load, Brogue replays the event stream up to that turn and then switches
to live play.

Usage examples:
    # Use most recent recording in default data dir, roll back 5 turns
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


def find_data_dir():
    """Locate the Brogue data directory via brew --prefix."""
    try:
        prefix = subprocess.check_output(["brew", "--prefix"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError("brew --prefix failed; specify --data-dir or --recording")
    if not os.path.isabs(prefix):
        raise RuntimeError(f"brew --prefix returned non-absolute path: {prefix!r}")
    data_dir = os.path.join(prefix, "var", "brogue")
    if not os.path.isdir(data_dir):
        raise RuntimeError(f"Brogue data directory not found: {data_dir}")
    return data_dir


def find_most_recent_recording(data_dir):
    """Find the most recently modified .broguerec file in data_dir."""
    best = None
    best_mtime = -1
    for entry in os.scandir(data_dir):
        if entry.name.endswith(".broguerec") and entry.is_file():
            mtime = entry.stat().st_mtime
            if mtime > best_mtime:
                best = entry.path
                best_mtime = mtime
    if not best:
        raise RuntimeError(f"No .broguerec files found in {data_dir}")
    return best


def main(argv):
    parser = argparse.ArgumentParser(
        description="Convert a Brogue recording into a save file rolled back N turns.",
        epilog=(
            "If no recording is specified, the most recent .broguerec in the "
            "data directory is used. The data directory is found via brew --prefix."
        ),
    )
    parser.add_argument(
        "-t", "--turns", type=int, default=5,
        help="Number of turns to roll back (default: 5).",
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
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Resolve data directory
    data_dir = args.data_dir

    if args.recording:
        recording_path = args.recording
        if not data_dir:
            data_dir = os.path.dirname(os.path.abspath(recording_path))
    else:
        if not data_dir:
            data_dir = find_data_dir()
        recording_path = find_most_recent_recording(data_dir)

    logging.info("Recording: %s", recording_path)

    # Read the file
    with open(recording_path, "rb") as f:
        data = bytearray(f.read())

    if len(data) < 36:
        return "File is too small to be a valid Brogue recording."

    original_turns = struct.unpack_from(">I", data, 24)[0]
    logging.info("Original turn count: %d", original_turns)

    if original_turns == 0:
        return "Recording has 0 turns; nothing to roll back."

    if args.turns >= original_turns:
        return (
            f"Cannot roll back {args.turns} turns: recording only has "
            f"{original_turns} turns."
        )

    new_turns = original_turns - args.turns
    logging.info("New turn count: %d (rolled back %d turns)", new_turns, args.turns)

    struct.pack_into(">I", data, 24, new_turns)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(os.path.basename(recording_path))[0]
        filename = f"{base}_recovered_turn{new_turns}.broguesave"
        if data_dir:
            output_path = os.path.join(data_dir, filename)
        else:
            output_path = filename

    if os.path.abspath(output_path) == os.path.abspath(recording_path):
        return "Output path is the same as input. Specify a different --output."

    # Write output; fail if file already exists to avoid accidental overwrites
    try:
        with open(output_path, "xb") as f:
            f.write(data)
    except FileExistsError:
        return f"Output file already exists: {output_path}"

    logging.info("Save written: %s", output_path)
    return 0


if __name__ == "__main__":
    exit(main(sys.argv[1:]))
