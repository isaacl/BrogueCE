#!/bin/bash
# Smoke tests for recover_save.py
# Verifies the script is importable and handles basic cases without crashing.

set -euo pipefail

SCRIPT="$(dirname "$0")/recover_save.py"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "=== Test: --help exits 0 ==="
python "$SCRIPT" --help >/dev/null

echo "=== Test: missing recording file exits non-zero ==="
if python "$SCRIPT" --recording "$TMPDIR/nonexistent.broguerec" 2>/dev/null; then
    echo "FAIL: should have exited non-zero"
    exit 1
fi

echo "=== Test: file too small (empty) ==="
touch "$TMPDIR/empty.broguerec"
if python "$SCRIPT" --recording "$TMPDIR/empty.broguerec" 2>/dev/null; then
    echo "FAIL: should have exited non-zero for empty file"
    exit 1
fi

echo "=== Test: file with 0 turns ==="
# Create a 36-byte file with turn count = 0 at offset 24
python -c "
import struct, sys
data = bytearray(36)
struct.pack_into('>I', data, 24, 0)
sys.stdout.buffer.write(data)
" > "$TMPDIR/zero_turns.broguerec"
output=$(python "$SCRIPT" --recording "$TMPDIR/zero_turns.broguerec" 2>&1 || true)
if ! echo "$output" | grep -q "0 turns"; then
    echo "FAIL: expected '0 turns' message, got: $output"
    exit 1
fi

echo "=== Test: rollback exceeds game turns ==="
python -c "
import struct, sys
data = bytearray(36)
struct.pack_into('>I', data, 24, 3)
sys.stdout.buffer.write(data)
" > "$TMPDIR/short.broguerec"
output=$(python "$SCRIPT" --recording "$TMPDIR/short.broguerec" --turns 5 2>&1 || true)
if ! echo "$output" | grep -q "exceeds"; then
    echo "FAIL: expected 'exceeds' message, got: $output"
    exit 1
fi

echo "=== Test: successful conversion ==="
python -c "
import struct, sys
data = bytearray(100)
struct.pack_into('>I', data, 24, 50)
sys.stdout.buffer.write(data)
" > "$TMPDIR/game.broguerec"
python "$SCRIPT" --recording "$TMPDIR/game.broguerec" --turns 5 --output "$TMPDIR/game.broguesave"
if [ ! -f "$TMPDIR/game.broguesave" ]; then
    echo "FAIL: output file not created"
    exit 1
fi
# Verify turn count in output
turn_count=$(python -c "
import struct, sys
with open('$TMPDIR/game.broguesave', 'rb') as f:
    data = f.read()
print(struct.unpack_from('>I', data, 24)[0])
")
if [ "$turn_count" != "45" ]; then
    echo "FAIL: expected turn count 45, got $turn_count"
    exit 1
fi

echo "=== Test: output file already exists ==="
if python "$SCRIPT" --recording "$TMPDIR/game.broguerec" --turns 5 --output "$TMPDIR/game.broguesave" 2>/dev/null; then
    echo "FAIL: should have failed on existing file"
    exit 1
fi

echo "=== All tests passed ==="
