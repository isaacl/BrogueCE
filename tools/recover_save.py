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
import os
import platform
import shutil
import struct
import subprocess
import sys
from pathlib import Path

HEADER_LENGTH = 36
TURN_OFFSET = 24  # howManyTurns: 4 bytes big-endian at offset 24
TURN_SIZE = 4

RECORDING_SUFFIX = ".broguerec"
SAVE_SUFFIX = ".broguesave"


def guess_data_dir():
    """Attempt to find the Brogue data directory."""
    system = platform.system()

    if system == "Darwin":
        # Try homebrew prefix
        try:
            prefix = subprocess.check_output(
                ["brew", "--prefix"], text=True, stderr=subprocess.DEVNULL
            ).strip()
            candidate = Path(prefix) / "var" / "brogue"
            if candidate.is_dir():
                return candidate
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        # Common fallback
        candidate = Path("/opt/homebrew/var/brogue")
        if candidate.is_dir():
            return candidate
        candidate = Path("/usr/local/var/brogue")
        if candidate.is_dir():
            return candidate
    elif system == "Linux":
        # XDG data home
        xdg = os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
        candidate = Path(xdg) / "brogue"
        if candidate.is_dir():
            return candidate
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidate = Path(appdata) / "brogue"
            if candidate.is_dir():
                return candidate

    return None


def find_most_recent_recording(data_dir):
    """Find the most recently modified .broguerec file in data_dir."""
    recordings = list(Path(data_dir).glob(f"*{RECORDING_SUFFIX}"))
    if not recordings:
        return None
    return max(recordings, key=lambda p: p.stat().st_mtime)


def read_turn_count(data):
    """Read the turn counter from the recording header."""
    return struct.unpack_from(">I", data, TURN_OFFSET)[0]


def write_turn_count(data, turns):
    """Write a new turn counter into the header."""
    struct.pack_into(">I", data, TURN_OFFSET, turns)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Brogue recording into a save file rolled back N turns.",
        epilog=(
            "If no recording is specified, the most recent .broguerec in the "
            "data directory is used. On macOS/Homebrew the data directory "
            "defaults to $(brew --prefix)/var/brogue."
        ),
    )
    parser.add_argument(
        "-t", "--turns",
        type=int,
        default=5,
        help="Number of turns to roll back (default: 5).",
    )
    parser.add_argument(
        "-r", "--recording",
        type=str,
        default=None,
        help="Path to the .broguerec file to convert.",
    )
    parser.add_argument(
        "-d", "--data-dir",
        type=str,
        default=None,
        help="Brogue data/saves directory.",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output path for the .broguesave file.",
    )

    args = parser.parse_args()

    # Resolve data directory
    data_dir = Path(args.data_dir) if args.data_dir else None

    # If recording is given, check if its parent looks like the data dir
    if args.recording:
        recording_path = Path(args.recording)
        if not recording_path.exists():
            sys.exit(f"Error: recording not found: {recording_path}")
        if data_dir is None:
            # Check if the recording lives in a plausible data dir
            parent = recording_path.parent
            if list(parent.glob(f"*{RECORDING_SUFFIX}")):
                data_dir = parent
    else:
        # No recording specified; need data dir to find one
        if data_dir is None:
            data_dir = guess_data_dir()
        if data_dir is None:
            sys.exit(
                "Error: could not determine data directory. "
                "Specify --data-dir or --recording."
            )
        if not data_dir.is_dir():
            sys.exit(f"Error: data directory does not exist: {data_dir}")

        recording_path = find_most_recent_recording(data_dir)
        if recording_path is None:
            sys.exit(f"Error: no {RECORDING_SUFFIX} files found in {data_dir}")

    print(f"Recording: {recording_path}")

    # Read the file
    data = bytearray(recording_path.read_bytes())

    if len(data) < HEADER_LENGTH:
        sys.exit("Error: file is too small to be a valid Brogue recording.")

    original_turns = read_turn_count(data)
    print(f"Original turn count: {original_turns}")

    if original_turns == 0:
        sys.exit("Error: recording has 0 turns; nothing to roll back.")

    rollback = args.turns
    if rollback >= original_turns:
        # Roll back to turn 1 at minimum
        rollback = original_turns - 1
        print(f"Warning: requested rollback exceeds turn count; rolling back to turn 1.")

    new_turns = original_turns - rollback
    if new_turns < 1:
        new_turns = 1

    print(f"New turn count: {new_turns} (rolled back {original_turns - new_turns} turns)")

    write_turn_count(data, new_turns)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Build a descriptive filename
        stem = recording_path.stem
        suffix = f"_recovered_turn{new_turns}{SAVE_SUFFIX}"
        filename = stem + suffix

        if data_dir:
            output_path = data_dir / filename
        else:
            output_path = Path.cwd() / filename

    # Don't overwrite the original
    if output_path.resolve() == recording_path.resolve():
        sys.exit("Error: output path is the same as input. Specify a different --output.")

    output_path.write_bytes(data)
    print(f"Save written: {output_path}")


if __name__ == "__main__":
    main()
