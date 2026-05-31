#!/usr/bin/env python3
"""lint_anti_backdoor.py — forbid backdoor phrases that re-introduce pattern-template grading.

These phrases are banned in SKILL.md, references/feedback-format.md, and
references/scoring.md because they anchor scoring to whether the learner used a
specific sentence template rather than whether the learner communicated clearly.
No "allowed section" exemptions exist — the phrases are blanket-forbidden.

Banned patterns (case-insensitive):
    1. didn't use (?:the )?suggested pattern
    2. should have used (?:the )?(?:suggested |recommended )?(?:template|pattern)
    3. pattern adherence
    4. failed to use (?:the )?(?:template|pattern)
    5. must use (?:the )?(?:suggested |recommended )?(?:template|pattern)

Usage:
    python3 lint_anti_backdoor.py [<skill-dir>]

`<skill-dir>` defaults to `nanobot/skills/english-train/` resolved from the
repo root (i.e. the directory containing this script's grandparent). Pass an
absolute path or a path relative to the current working directory to override.

Exit codes:
    0 — no forbidden phrases found
    1 — one or more violations found (violations printed to stdout)
    2 — usage error
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_BANNED: list[re.Pattern[str]] = [
    re.compile(r"didn't use (?:the )?suggested pattern", re.IGNORECASE),
    re.compile(
        r"should have used (?:the )?(?:suggested |recommended )?(?:template|pattern)",
        re.IGNORECASE,
    ),
    re.compile(r"pattern adherence", re.IGNORECASE),
    re.compile(r"failed to use (?:the )?(?:template|pattern)", re.IGNORECASE),
    re.compile(
        r"must use (?:the )?(?:suggested |recommended )?(?:template|pattern)",
        re.IGNORECASE,
    ),
]

# Files to scan, relative to the skill dir.
_SCAN_TARGETS = [
    Path("SKILL.md"),
    Path("references") / "feedback-format.md",
    Path("references") / "scoring.md",
]


def lint_file(path: Path) -> list[str]:
    """Return violation strings for `path`, empty if clean."""
    lines = path.read_text(encoding="utf-8").splitlines()
    violations: list[str] = []

    for lineno, line in enumerate(lines, start=1):
        for pattern in _BANNED:
            m = pattern.search(line)
            if m:
                violations.append(f"{path}:{lineno}: forbidden phrase '{m.group(0)}'")
                # One violation per line per pattern — don't break; catch all patterns.

    return violations


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: lint_anti_backdoor.py [<skill-dir>]", file=sys.stderr)
        return 2

    if len(sys.argv) == 2:
        skill_dir = Path(sys.argv[1])
    else:
        # This script lives at nanobot/skills/english-train/scripts/lint_anti_backdoor.py,
        # so its grandparent is the skill dir.
        skill_dir = Path(__file__).resolve().parents[1]

    if not skill_dir.is_dir():
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 2

    all_violations: list[str] = []

    for relative_target in _SCAN_TARGETS:
        target = skill_dir / relative_target
        if not target.is_file():
            print(f"warning: {target} not found, skipping", file=sys.stderr)
            continue
        all_violations.extend(lint_file(target))

    for v in all_violations:
        print(v)

    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
