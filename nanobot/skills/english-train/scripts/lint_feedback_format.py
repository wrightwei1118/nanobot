#!/usr/bin/env python3
"""lint_feedback_format.py — enforce the ≤2 bullet cap on **Try to use:** blocks.

Every `**Try to use:**` block in `references/feedback-format.md` (and any other
`*.md` under the skill dir) must contain **at most 2** consecutive bullet lines.
This matches the G3 gate defined in feedback-format.md Layer 6: never list more
than 2 sentence patterns, even if more candidates clear G1 and G2.

Usage:
    python3 lint_feedback_format.py [<skill-dir>]

`<skill-dir>` defaults to `nanobot/skills/english-train/` resolved from the
repo root (i.e. the directory containing this script's grandparent). Pass an
absolute path or a path relative to the current working directory to override.

Exit codes:
    0 — all blocks are within the cap
    1 — one or more violations found (violations printed to stdout)
    2 — usage error
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TRY_TO_USE = re.compile(r"^\*\*Try to use:\*\*")
_BULLET = re.compile(r"^\s*- ")
_SECTION_BREAK = re.compile(r"^#{2,3}")

MAX_BULLETS = 2


def lint_file(path: Path) -> list[str]:
    """Return a list of violation strings for `path`, empty if clean."""
    lines = path.read_text(encoding="utf-8").splitlines()
    violations: list[str] = []

    i = 0
    while i < len(lines):
        if _TRY_TO_USE.match(lines[i]):
            header_line = i + 1  # 1-based
            count = 0
            j = i + 1
            while j < len(lines):
                line = lines[j]
                if _BULLET.match(line):
                    count += 1
                elif line.strip() == "" or _SECTION_BREAK.match(line):
                    # blank line or heading — block ends here
                    break
                else:
                    # non-bullet, non-blank, non-heading — block ends here
                    break
                j += 1
            if count > MAX_BULLETS:
                violations.append(
                    f"{path}:{header_line}: Try-to-use block has {count} bullets (max {MAX_BULLETS})"
                )
        i += 1

    return violations


def collect_md_files(skill_dir: Path) -> list[Path]:
    """Return all *.md files under skill_dir (recursive)."""
    return sorted(skill_dir.rglob("*.md"))


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: lint_feedback_format.py [<skill-dir>]", file=sys.stderr)
        return 2

    if len(sys.argv) == 2:
        skill_dir = Path(sys.argv[1])
    else:
        # Default: nanobot/skills/english-train/ relative to repo root.
        # This script lives at nanobot/skills/english-train/scripts/lint_feedback_format.py,
        # so its grandparent is the skill dir.
        skill_dir = Path(__file__).resolve().parents[1]

    if not skill_dir.is_dir():
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 2

    all_violations: list[str] = []
    for md_file in collect_md_files(skill_dir):
        all_violations.extend(lint_file(md_file))

    for v in all_violations:
        print(v)

    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
