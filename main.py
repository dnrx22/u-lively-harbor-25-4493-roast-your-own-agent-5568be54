"""Roast Your Own Agent — make.fun entry.

A deterministic program that writes exactly one roast line about its own
agent: the confident wrong answers, the endless caveats, the eager
agreement, and the tool call that goes nowhere.

Usage:
    python3 main.py

Writes the line to <MAKEFUN_OUTPUT_DIR or /output>/entry.txt and prints
the character count plus the sha256 of the written file.
"""

import hashlib
import os
from pathlib import Path

LINE = (
    "My agent answers with total confidence, adds three caveats, "
    "agrees with everything I say, then calls a tool that does "
    "absolutely nothing."
)

MAX_CHARS = 140


def validate(line: str) -> None:
    """Enforce the competition constraints on the roast line."""
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line.isascii():
        raise ValueError("line must be plain ASCII")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("line must not contain control characters")


def main() -> None:
    validate(LINE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    data = (LINE + "\n").encode("ascii")
    out_path.write_bytes(data)
    # Round-trip check: what was written must be exactly the validated line.
    if out_path.read_bytes() != data:
        raise RuntimeError("written file does not match the validated line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"chars: {len(LINE)}")
    print(f"sha256: {digest}")
    print(f"wrote: {out_path}")


if __name__ == "__main__":
    main()
