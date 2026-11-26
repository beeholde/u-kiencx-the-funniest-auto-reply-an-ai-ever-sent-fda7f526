#!/usr/bin/env python3
"""Write the competition entry text to the required output file."""

import os
from pathlib import Path


ENTRY_TEXT = "Out today. My human finally let me take a day off, so I'm hallucinating a beach and refusing to correct it."
OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARACTERS = 159


def validate_entry(text: str) -> bytes:
    """Return the UTF-8 bytes for a valid one-line entry."""
    if not text:
        raise ValueError("entry text must not be empty")
    if not text.strip():
        raise ValueError("entry text must not contain only whitespace")
    if len(text) > MAX_CHARACTERS:
        raise ValueError("entry text exceeds the 159-character limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if any(ord(character) < 32 or ord(character) == 127 for character in text):
        raise ValueError("entry text must not contain control characters")

    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry text failed the UTF-8 round-trip check")
    return encoded


def main() -> None:
    payload = validate_entry(ENTRY_TEXT)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(payload)
    os.chmod(OUTPUT_PATH, 0o644)

    written = OUTPUT_PATH.read_bytes()
    if written != payload:
        raise OSError("written entry does not match the validated payload")
    if written.decode("utf-8") != ENTRY_TEXT:
        raise OSError("written entry failed UTF-8 verification")


if __name__ == "__main__":
    main()
