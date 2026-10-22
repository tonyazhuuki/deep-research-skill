#!/usr/bin/env python3
"""Fail when private-vault fingerprints enter the public release tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__"}
ALLOW_NAME_IN = {Path("LICENSE")}
FORBIDDEN_LITERALS = (
    "00_" + "vision/",
    "01_" + "library/",
    "03_" + "blog/",
    "04_" + "therapy/",
    "05_" + "personal/",
    "06_" + "projects/",
    "90_" + "meta/",
    "Pl" + "aud",
    "personal" + "-os",
    "Cu " + "77.6",
    "HOMA-IR " + "~1.06",
    "prefer not " + "isotretinoin",
    "WHOOP MCP " + "Strain.json",
)
PERSON_NAME = "Ton" + "ya"
PERSON_NAME_RE = re.compile(rf"\b{re.escape(PERSON_NAME)}\b", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def iter_text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or SKIP_PARTS.intersection(path.parts):
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


def validate() -> list[str]:
    errors: list[str] = []
    for path, text in iter_text_files():
        relative = path.relative_to(ROOT)
        for marker in FORBIDDEN_LITERALS:
            if marker.lower() in text.lower():
                errors.append(f"{relative}: forbidden private marker {marker!r}")
        if EMAIL_RE.search(text):
            errors.append(f"{relative}: public email address detected")
        if PERSON_NAME_RE.search(text) and relative not in ALLOW_NAME_IN:
            errors.append(f"{relative}: personal name outside legal attribution")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("INVALID PUBLIC RELEASE")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID PUBLIC RELEASE: no private-vault fingerprints detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
