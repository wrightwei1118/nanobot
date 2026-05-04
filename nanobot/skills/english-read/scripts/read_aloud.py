#!/usr/bin/env python3
"""
english-read skill runtime — Leitner spaced repetition + state + history + rendering.

The skill's LLM side only needs to:
  1. Match trigger words → decide subcommand (select / confirm).
  2. Run this script.
  3. Echo stdout to the user verbatim.

Deterministic work (Leitner box management, sidecar sync, HISTORY append,
read-back verification, completion-block rendering) lives here.

Data files (all under NANOBOT_READ_DATA_DIR, default /root/.nanobot/workspace/memory):
  - readings.md          : written by english-train, read-only here
  - readings-state.json  : sidecar, per-entry Leitner state (box + due date)
  - read-state.json      : session state (last push + confirmation flag)
  - HISTORY.md           : shared audit log (english-train + english-read both append)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(os.environ.get("NANOBOT_READ_DATA_DIR", "/root/.nanobot/workspace/memory"))
READINGS = DATA_DIR / "readings.md"
SIDECAR = DATA_DIR / "readings-state.json"
SESSION_STATE = DATA_DIR / "read-state.json"
HISTORY = DATA_DIR / "HISTORY.md"

# Leitner: after confirmation on Box N, next review is +INTERVALS[N+1] days.
# Box 5 confirmed → graduated (never picked again).
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
GRADUATED = 6
DEFAULT_CAP = 3       # no overdue → normal daily cap
EXTENDED_CAP = 4      # any overdue → bump cap to clear backlog faster
OVERDUE_RESERVED = 2  # up to this many slots filled from overdue pool first

ENTRY_HEADER_RE = re.compile(
    r"^##\s+\[(?P<date>\d{4}-\d{2}-\d{2})\]\s+Topic:\s+(?P<topic>.+?)\s+\|\s+Round\s+(?P<round>\d+):\s+(?P<round_topic>.+?)\s*$"
)


@dataclass
class Entry:
    date: str
    topic: str
    round: int
    round_topic: str
    complete: str
    polished: str

    @property
    def key(self) -> str:
        return f"{self.date}|{self.topic}|{self.round}"

    def header(self) -> str:
        return f"[{self.date}] Topic: {self.topic} | Round {self.round}: {self.round_topic}"


# --------------------------------------------------------------------------
# readings.md parsing
# --------------------------------------------------------------------------

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
        block = lines[i + 1:next_i]
        entries.append(Entry(
            date=g["date"],
            topic=g["topic"].strip(),
            round=int(g["round"]),
            round_topic=g["round_topic"].strip(),
            complete=_extract_block(block, "Complete Version"),
            polished=_extract_block(block, "Polished Version"),
        ))
        i = next_i
    return entries


def _extract_block(block_lines: list[str], label: str) -> str:
    needle = f"**{label}:**"
    for j, line in enumerate(block_lines):
        if line.strip() == needle:
            buf: list[str] = []
            for k in range(j + 1, len(block_lines)):
                stripped = block_lines[k].strip()
                if re.match(r"^\*\*.+:\*\*$", stripped):
                    break
                buf.append(block_lines[k])
            return "\n".join(buf).strip("\n").rstrip()
    return ""


def _find_next_header(lines: list[str], start: int) -> int:
    for j in range(start, len(lines)):
        if ENTRY_HEADER_RE.match(lines[j]):
            return j
    return len(lines)


# --------------------------------------------------------------------------
# Sidecar state
# --------------------------------------------------------------------------

def load_sidecar() -> dict[str, dict]:
    if not SIDECAR.exists():
        return {}
    return json.loads(SIDECAR.read_text())


def save_sidecar(sidecar: dict[str, dict]) -> dict[str, dict]:
    SIDECAR.parent.mkdir(parents=True, exist_ok=True)
    SIDECAR.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2))
    return json.loads(SIDECAR.read_text())


def sync_sidecar(entries: list[Entry], sidecar: dict[str, dict], today: date) -> dict[str, dict]:
    """Add box:1, due:today for new entries; prune entries no longer in readings.md."""
    current_keys = {e.key for e in entries}
    for e in entries:
        if e.key not in sidecar:
            sidecar[e.key] = {"box": 1, "due": today.isoformat()}
    # Prune dropped entries (english-train's TTL deletes them)
    for stale in [k for k in sidecar if k not in current_keys]:
        del sidecar[stale]
    return sidecar


def advance_boxes(keys: list[str], sidecar: dict[str, dict], today: date) -> None:
    """Promotion on confirmation. Box N (N<5) → N+1 with due = today + INTERVALS[N+1].
    Box 5 confirmed → GRADUATED (never picked again)."""
    for k in keys:
        st = sidecar.get(k)
        # Silent skip: entry may have been TTL-deleted by english-train between push and confirm
        if st is None:
            continue
        box = st["box"]
        if box >= 5:
            st["box"] = GRADUATED
            st["due"] = today.isoformat()
        else:
            st["box"] = box + 1
            st["due"] = (today + timedelta(days=INTERVALS[box + 1])).isoformat()


# --------------------------------------------------------------------------
# Selection — Leitner
# --------------------------------------------------------------------------

def due_entries(entries: list[Entry], sidecar: dict[str, dict], today: date) -> list[tuple[Entry, int, str]]:
    """Return (entry, box, due) for entries with box < GRADUATED AND due <= today."""
    out: list[tuple[Entry, int, str]] = []
    for e in entries:
        st = sidecar.get(e.key)
        if st is None or st["box"] >= GRADUATED:
            continue
        if date.fromisoformat(st["due"]) <= today:
            out.append((e, st["box"], st["due"]))
    return out


def rank_due(due: list[tuple[Entry, int, str]]) -> list[Entry]:
    """
    Priority: higher box first, then oldest due first within the same box.
    Rationale: Box 5 items are scarce (one per ~54 days of training) and carry
    more accumulated review investment; starving a low-box item costs 1 day
    at most since english-train keeps feeding Box 1. See Leitner scheduling notes.
    """
    return [e for e, _, _ in sorted(due, key=lambda x: (-x[1], x[2]))]


def select_entries(entries: list[Entry], sidecar: dict[str, dict], today: date) -> list[Entry]:
    """
    Selection rules:
      - 0 overdue (all due items have due == today) → return rank_due(due)[:DEFAULT_CAP]
      - ≥1 overdue (due < today) → return up to EXTENDED_CAP entries:
          * First slots: up to OVERDUE_RESERVED entries picked from the overdue pool,
            ranked by (-box, due). These appear FIRST in the output.
          * Remaining slots: filled from (non-picked overdue ∪ today-due),
            ranked by (-box, due).
      - If fewer than EXTENDED_CAP candidates exist in total, return what you have.
    """
    due = due_entries(entries, sidecar, today)
    if not due:
        return []
    today_iso = today.isoformat()
    overdue = [row for row in due if row[2] < today_iso]
    if not overdue:
        return rank_due(due)[:DEFAULT_CAP]

    priority = rank_due(overdue)[:OVERDUE_RESERVED]
    picked_keys = {e.key for e in priority}
    remaining = [row for row in due if row[0].key not in picked_keys]
    fill = rank_due(remaining)[:EXTENDED_CAP - len(priority)]
    return priority + fill


# --------------------------------------------------------------------------
# Session state (last push + confirmation flag)
# --------------------------------------------------------------------------

def load_session() -> dict | None:
    if not SESSION_STATE.exists():
        return None
    return json.loads(SESSION_STATE.read_text())


def save_session(state: dict) -> dict:
    SESSION_STATE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    return json.loads(SESSION_STATE.read_text())


def append_history(line: str) -> str:
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(line + "\n")
    return HISTORY.read_text().rstrip("\n").splitlines()[-1]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_session(entries: list[Entry], sidecar: dict[str, dict], *, is_repush: bool) -> str:
    out: list[str] = []
    if is_repush:
        out.append("上次推送的内容还没确认，再来一遍 👇")
        out.append("")
    for i, e in enumerate(entries, 1):
        box = sidecar.get(e.key, {}).get("box", 1)
        out.append(f"### [{i}/{len(entries)}] — {e.topic} (Round {e.round}, {e.date}) · Box {box}")
        out.append("")
        out.append("**Complete Version (read aloud first):**")
        out.append(e.complete)
        out.append("")
        out.append("**Polished Version (then read this):**")
        out.append(e.polished)
        out.append("")
    out.append(f"Done! {len(entries)} entries read today.")
    return "\n".join(out)


def render_block(session: dict, history_line: str | None, *, confirmation_only: bool) -> str:
    lines = ["---", "📝 State Sync", f"- last_push_date: {session['last_push_date']}"]
    if not confirmation_only:
        dates = ", ".join(e["date"] for e in session["last_push_entries"])
        lines.append(f"- entries: {len(session['last_push_entries'])} ({dates})")
    lines.append(f"- confirmed: {str(session['confirmed']).lower()}")
    if history_line:
        ts = history_line.split("]", 1)[0].lstrip("[")
        lines.append(f"- history: {ts} ✓")
    lines.append("---")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Subcommands
# --------------------------------------------------------------------------

def cmd_select(trigger: str) -> int:
    if not READINGS.exists():
        print("readings.md 不存在 —— 先跑几次 `english-train` 生成素材再来朗读。")
        return 1
    entries = parse_readings(READINGS.read_text())
    if not entries:
        print("readings.md 里没有可读的条目 —— 先跑 `english-train`。")
        return 1

    today = date.today()
    sidecar = sync_sidecar(entries, load_sidecar(), today)
    prev = load_session()

    is_repush = False
    if prev and not prev["confirmed"]:
        if trigger == "cron":
            # Re-push same entries if all still resolvable; otherwise fall through to new selection.
            picked = _resolve_entries(prev["last_push_entries"], entries)
            if len(picked) == len(prev["last_push_entries"]):
                is_repush = True
            else:
                picked = select_entries(entries, sidecar, today)
        else:
            # Manual trigger = implicit confirm of prior push → advance boxes, then pick new
            advance_boxes([_k(r) for r in prev["last_push_entries"]], sidecar, today)
            picked = select_entries(entries, sidecar, today)
    else:
        picked = select_entries(entries, sidecar, today)

    if not picked:
        print("今天没有到期的条目可以朗读。都复习完了或者还没到复习日 🎉")
        return 0

    sidecar = save_sidecar(sidecar)
    session = {
        "last_push_date": today.isoformat(),
        "last_push_entries": [
            {"date": e.date, "topic": e.topic, "round": e.round} for e in picked
        ],
        "confirmed": False,
    }
    verified = save_session(session)
    mode = "re-push" if is_repush else "new"
    dates = ", ".join(e.date for e in picked)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    history_line = append_history(
        f"[{ts}] english-read | Entries read: {len(picked)} | Dates: {dates} | Mode: {mode}"
    )

    print(render_session(picked, sidecar, is_repush=is_repush))
    print()
    print(render_block(verified, history_line, confirmation_only=False))
    return 0


def _k(ref: dict) -> str:
    return f"{ref['date']}|{ref['topic']}|{ref['round']}"


def _resolve_entries(refs: list[dict], entries: list[Entry]) -> list[Entry]:
    idx = {e.key: e for e in entries}
    return [idx[_k(r)] for r in refs if _k(r) in idx]


def cmd_confirm() -> int:
    prev = load_session()
    if not prev:
        print("还没有推送记录可以确认。")
        return 1
    today = date.today()
    sidecar = load_sidecar()
    advance_boxes([_k(r) for r in prev["last_push_entries"]], sidecar, today)
    save_sidecar(sidecar)

    prev["confirmed"] = True
    verified = save_session(prev)
    print("已确认，条目晋级。明天会推送新内容。")
    print()
    print(render_block(verified, history_line=None, confirmation_only=True))
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--trigger", choices=["manual", "cron"], default="manual")
    sub.add_parser("confirm")
    args = p.parse_args()
    if args.cmd == "select":
        return cmd_select(args.trigger)
    if args.cmd == "confirm":
        return cmd_confirm()
    return 2


if __name__ == "__main__":
    sys.exit(main())
