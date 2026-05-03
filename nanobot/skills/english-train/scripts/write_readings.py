#!/usr/bin/env python3
"""
english-train skill runtime — writes readings.md entries and HISTORY.md summaries.

The skill's LLM side only needs to:
  1. After each round's feedback layers, call `add-round` with metadata + stdin.
  2. After End-of-Session Scoring, call `history` with the summary fields.
  3. Echo the one-line confirmation.

Deterministic work (format rendering, key-collision overwrite, 60-day TTL,
content validation, history rendering) lives here.

Data files (all under NANOBOT_READ_DATA_DIR, default /root/.nanobot/workspace/memory,
shared with english-read):
  - readings.md : written by this script, read by read_aloud.py
  - HISTORY.md  : shared audit log (english-train + english-read both append)

Writing contract (read_aloud.py depends on this — do not break):
  - Header:       ## [YYYY-MM-DD] Topic: X | Round N: Y
  - Block labels: `**Complete Version:**` / `**Polished Version:**` each on its own line
  - Block content must NOT contain other `**...:**` standalone lines
    (read_aloud.py would parse them as a new block boundary and truncate the entry)
  - Key (date, topic, round) is unique; re-submission overwrites (latest wins)
  - TTL: entries older than 60 days (by `date` field) are pruned on every write
    60 >= 54 (Leitner 1+3+7+14+30 graduation window) + buffer for missed confirmations
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(os.environ.get("NANOBOT_READ_DATA_DIR", "/root/.nanobot/workspace/memory"))
READINGS = DATA_DIR / "readings.md"
HISTORY = DATA_DIR / "HISTORY.md"

TTL_DAYS = 60

ENTRY_HEADER_RE = re.compile(
    r"^##\s+\[(?P<date>\d{4}-\d{2}-\d{2})\]\s+Topic:\s+(?P<topic>.+?)\s+\|\s+Round\s+(?P<round>\d+):\s+(?P<round_topic>.+?)\s*$"
)
BLOCK_LABEL_RE = re.compile(r"^\s*\*\*.+:\*\*\s*$")

COMPLETE_DELIM = "===COMPLETE==="
POLISHED_DELIM = "===POLISHED==="


@dataclass
class Entry:
    date: str
    topic: str
    round: int
    round_topic: str
    complete: str
    polished: str

    @property
    def key(self) -> tuple[str, str, int]:
        return (self.date, self.topic, self.round)

    def render(self) -> str:
        return (
            f"## [{self.date}] Topic: {self.topic} | Round {self.round}: {self.round_topic}\n"
            "\n"
            "**Complete Version:**\n"
            f"{self.complete}\n"
            "\n"
            "**Polished Version:**\n"
            f"{self.polished}\n"
            "\n"
        )


# ---------------------------------------------------------------------------
# readings.md parse / render (mirrors read_aloud.py parser)
# ---------------------------------------------------------------------------

def parse_readings(text: str) -> list[Entry]:
    entries: list[Entry] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = ENTRY_HEADER_RE.match(lines[i])
        if not m:
            i += 1
            continue
        g = m.groupdict()
        next_i = _find_next_header(lines, i + 1)
        block = lines[i + 1 : next_i]
        entries.append(
            Entry(
                date=g["date"],
                topic=g["topic"].strip(),
                round=int(g["round"]),
                round_topic=g["round_topic"].strip(),
                complete=_extract_block(block, "Complete Version"),
                polished=_extract_block(block, "Polished Version"),
            )
        )
        i = next_i
    return entries


def _extract_block(block_lines: list[str], label: str) -> str:
    needle = f"**{label}:**"
    for j, line in enumerate(block_lines):
        if line.strip() == needle:
            buf: list[str] = []
            for k in range(j + 1, len(block_lines)):
                if re.match(r"^\*\*.+:\*\*$", block_lines[k].strip()):
                    break
                buf.append(block_lines[k])
            return "\n".join(buf).strip("\n").rstrip()
    return ""


def _find_next_header(lines: list[str], start: int) -> int:
    for j in range(start, len(lines)):
        if ENTRY_HEADER_RE.match(lines[j]):
            return j
    return len(lines)


def render_all(entries: list[Entry]) -> str:
    if not entries:
        return ""
    return "".join(e.render() for e in entries).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Validation — fail loud on contract violations
# ---------------------------------------------------------------------------

def validate_date(s: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        sys.exit(f"error: --date must be YYYY-MM-DD, got {s!r}")
    try:
        date.fromisoformat(s)
    except ValueError:
        sys.exit(f"error: --date is not a valid date: {s!r}")
    return s


def validate_topic(s: str) -> str:
    s = s.strip()
    if not s:
        sys.exit("error: --topic cannot be empty")
    if "\n" in s:
        sys.exit("error: --topic cannot contain newlines")
    # ' | Round ' in topic would confuse ENTRY_HEADER_RE (non-greedy but still risky).
    if " | Round " in s:
        sys.exit("error: --topic cannot contain ' | Round ' (conflicts with header parser)")
    return s


def validate_round_topic(s: str) -> str:
    s = s.strip()
    if not s:
        sys.exit("error: --round-topic cannot be empty")
    if "\n" in s:
        sys.exit("error: --round-topic cannot contain newlines")
    return s


def validate_content(label: str, s: str) -> str:
    # Reject lines that look like block markers — read_aloud.py would parse them as
    # new block boundaries and truncate this entry. Pre-existing fragility from the
    # LLM-only era; surfacing it loudly here prevents silent data corruption.
    for line in s.splitlines():
        if BLOCK_LABEL_RE.match(line):
            sys.exit(
                f"error: {label} contains a line matching `**...:**` which conflicts with "
                f"read_aloud.py's block parser: {line!r}"
            )
    cleaned = s.strip("\n").rstrip()
    if not cleaned:
        sys.exit(f"error: {label} is empty")
    return cleaned


def split_stdin(text: str) -> tuple[str, str]:
    """Split stdin into (complete, polished) using the delimiter sentinels."""
    if COMPLETE_DELIM not in text or POLISHED_DELIM not in text:
        sys.exit(
            f"error: stdin must contain both {COMPLETE_DELIM} and {POLISHED_DELIM} delimiters"
        )
    c_idx = text.index(COMPLETE_DELIM)
    p_idx = text.index(POLISHED_DELIM)
    if c_idx > p_idx:
        sys.exit(f"error: {COMPLETE_DELIM} must appear before {POLISHED_DELIM}")
    complete = text[c_idx + len(COMPLETE_DELIM) : p_idx]
    polished = text[p_idx + len(POLISHED_DELIM) :]
    return complete, polished


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_add_round(args: argparse.Namespace) -> int:
    raw = sys.stdin.read()
    complete_raw, polished_raw = split_stdin(raw)
    entry = Entry(
        date=validate_date(args.date),
        topic=validate_topic(args.topic),
        round=args.round,
        round_topic=validate_round_topic(args.round_topic),
        complete=validate_content("Complete Version", complete_raw),
        polished=validate_content("Polished Version", polished_raw),
    )

    existing = parse_readings(READINGS.read_text()) if READINGS.exists() else []
    before_len = len(existing)

    # Key collision → overwrite (retry semantics: latest feedback is authoritative)
    existing = [e for e in existing if e.key != entry.key]
    replaced = len(existing) < before_len
    existing.append(entry)

    # TTL prune by `date` field (not file mtime) — so a learner returning after a
    # break ages entries by training date, not by when the script last ran.
    cutoff = (date.today() - timedelta(days=TTL_DAYS)).isoformat()
    kept = [e for e in existing if e.date >= cutoff]
    pruned = len(existing) - len(kept)

    READINGS.parent.mkdir(parents=True, exist_ok=True)
    READINGS.write_text(render_all(kept))

    action = "replaced" if replaced else "added"
    print(
        f"✓ readings.md: {action} [{entry.date}] {entry.topic} / Round {entry.round} "
        f"(kept {len(kept)} entries, pruned {pruned})"
    )
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    ordinal = _ordinal(args.today_count)
    line = (
        f"[{ts}] english-train | Session {args.session_n} ({ordinal} today) | "
        f"Topic: {args.topic} | "
        f"Scores: F{args.fluency} G{args.grammar} T{args.technical} | "
        f"Status: {args.status} | Top issue: {args.top_issue}"
    )
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(line + "\n")
    print(f"✓ HISTORY.md: recorded Session {args.session_n} ({ordinal} today)")
    return 0


def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add-round", help="append one round's entry to readings.md")
    add.add_argument("--date", required=True, help="YYYY-MM-DD")
    add.add_argument("--topic", required=True)
    add.add_argument("--round", type=int, required=True)
    add.add_argument("--round-topic", required=True, dest="round_topic")
    add.set_defaults(func=cmd_add_round)

    hist = sub.add_parser("history", help="append a session summary line to HISTORY.md")
    hist.add_argument("--session-n", type=int, required=True, dest="session_n")
    hist.add_argument("--today-count", type=int, required=True, dest="today_count")
    hist.add_argument("--topic", required=True)
    hist.add_argument("--fluency", type=int, required=True)
    hist.add_argument("--grammar", type=int, required=True)
    hist.add_argument("--technical", type=int, required=True)
    hist.add_argument("--status", required=True, choices=["finished", "unfinished"])
    hist.add_argument("--top-issue", required=True, dest="top_issue")
    hist.set_defaults(func=cmd_history)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
