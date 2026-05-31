#!/usr/bin/env python3
"""lint_round_references.py — detect hard-coded 5-Round / Round-5 references outside
allowed sections in english-train skill files.

Why this lint exists: plan §3 generalised all hard-coded "5 rounds" or "Round 5"
references to per-category counts so the skill works for any number of rounds.
Any new prose that re-introduces a numeric tie to exactly 5 would silently break
the abstraction. We fail loudly here instead so the regression is caught on the
PR that introduces it.

Allowed locations: inside a section whose H2 or H3 heading contains
"concept-explanation" or "comparison" (case-insensitive). Those sections legitimately
describe the category definitions, so references to specific round counts are fine.

Banned patterns (case-insensitive):
  \\b5[- ]Round\\b        — "5-Round", "5 Round"
  \\bRound\\s*5\\b        — "Round 5", "Round5"
  \\bafter\\s+Round\\s+5\\b — "after Round 5"
  \\bexactly\\s+5\\s+rounds\\b — "exactly 5 rounds"

Files scanned:
  <skill-dir>/SKILL.md
  <skill-dir>/references/feedback-format.md
  <skill-dir>/references/topics-context/*.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Patterns that are banned outside scoped sections.
_BANNED_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\b5[- ]Round\b",
        r"\bRound\s*5\b",
        r"\bafter\s+Round\s+5\b",
        r"\bexactly\s+5\s+rounds\b",
    )
)

# H2 or H3 heading regex — used to track the current section scope.
_HEADING_RE = re.compile(r"^#{2,3}\s+(.+)")


def _is_scoped_heading(heading_text: str) -> bool:
    """Return True if this heading opens an allowed section."""
    lower = heading_text.lower()
    return "concept-explanation" in lower or "comparison" in lower


def lint_file(path: Path) -> list[str]:
    """Lint a single file. Returns a list of violation message strings."""
    violations: list[str] = []
    in_allowed_section = False

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        heading_match = _HEADING_RE.match(raw_line)
        if heading_match:
            # H2/H3 headings update the section scope; H1 does not.
            in_allowed_section = _is_scoped_heading(heading_match.group(1))
            continue

        if in_allowed_section:
            continue

        for pattern in _BANNED_PATTERNS:
            if pattern.search(raw_line):
                violations.append(
                    f"{path}:{lineno}: forbidden pattern {pattern.pattern!r} outside scoped section"
                )

    return violations


def _default_skill_dir() -> Path:
    """Resolve the skill dir relative to this script.

    The script lives at `nanobot/skills/english-train/scripts/lint_round_references.py`,
    so the skill dir is `../` (i.e. `nanobot/skills/english-train/`) from there.
    """
    return Path(__file__).resolve().parent.parent


def _collect_files(skill_dir: Path) -> list[Path]:
    """Build the list of files to scan, skipping missing ones with a warning."""
    candidates: list[Path] = [
        skill_dir / "SKILL.md",
        skill_dir / "references" / "feedback-format.md",
    ]
    topics_dir = skill_dir / "references" / "topics-context"
    if topics_dir.is_dir():
        candidates.extend(sorted(topics_dir.glob("*.md")))
    else:
        print(
            f"warning: topics-context directory not found: {topics_dir}",
            file=sys.stderr,
        )

    present: list[Path] = []
    for p in candidates:
        if p.exists():
            present.append(p)
        else:
            print(f"warning: file not found, skipping: {p}", file=sys.stderr)
    return present


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print(
            "Usage: lint_round_references.py [<skill-dir>]",
            file=sys.stderr,
        )
        return 2

    skill_dir = Path(args[0]).resolve() if args else _default_skill_dir()
    if not skill_dir.is_dir():
        print(f"error: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    files = _collect_files(skill_dir)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(lint_file(f))

    for msg in all_violations:
        print(msg)

    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
