#!/usr/bin/env python3
"""Validate the standalone Codex skill package and portability boundary."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REQUIRED = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/pipeline.md",
    "references/evidence.md",
    "references/frameworks.md",
    "references/domain-adapters.md",
    "references/run-contract.md",
    "scripts/validate_skill.py",
    "scripts/validate_run.py",
}
FORBIDDEN = (
    "." + "claude/",
    "04_" + "therapy/",
    "05_" + "personal/",
    "06_" + "projects/" + "_meetings/",
    "zhuuki" + "@gmail.com",
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in sorted(REQUIRED):
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    skill_path = root / "SKILL.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append("SKILL.md has invalid YAML frontmatter")
        else:
            try:
                frontmatter = yaml.safe_load(match.group(1))
            except yaml.YAMLError as exc:
                errors.append(f"SKILL.md frontmatter is invalid YAML: {exc}")
            else:
                if set(frontmatter or {}) != {"name", "description"}:
                    errors.append("SKILL.md frontmatter must contain only name and description")
                if (frontmatter or {}).get("name") != "deep-research":
                    errors.append("SKILL.md name must be deep-research")
        if len(text.splitlines()) > 500:
            errors.append("SKILL.md exceeds 500 lines")

    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in FORBIDDEN:
            if marker.lower() in text.lower():
                errors.append(f"non-portable marker {marker!r} in {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    errors = validate(root)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
