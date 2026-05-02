---
name: english-read
description: "Daily read-aloud practice using Leitner spaced repetition. Triggers: '朗读练习' / 'read aloud' / '开始朗读' to start a session. '收到' / '已读' / 'done' / 'got it' to confirm last push. Runs scripts/read_aloud.py which owns selection, state, and rendering."
---

# English Read — Daily Read-Aloud Practice

Thin wrapper around `{baseDir}/scripts/read_aloud.py`. The script owns all business logic: Leitner box scheduling, per-entry state sync, session state, HISTORY append, read-back verification, and rendering of both the entries and the completion block.

Your job as the skill:

1. Match the trigger phrase → pick the subcommand.
2. Ensure the daily cron job exists.
3. Run the script and echo its stdout verbatim.

## Triggers → Command

| Learner says | Command |
|---|---|
| `朗读练习` / `read aloud` / `开始朗读` | `python3 {baseDir}/scripts/read_aloud.py select --trigger=manual` |
| Cron `daily-english-read` fires | `python3 {baseDir}/scripts/read_aloud.py select --trigger=cron` |
| `收到` / `已读` / `done` / `got it` | `python3 {baseDir}/scripts/read_aloud.py confirm` |

## Before First Run — Register Cron

Call `cron(action="list")` and look for a job named `daily-english-read`.
- If missing: `cron(action="add", name="daily-english-read", message="朗读练习", cron_expr="0 6 * * *", tz="Asia/Shanghai")`
- If present: skip.

## Running the Script

- Echo stdout verbatim as your response — it already contains the full user-facing output (entry text, box labels, completion block).
- Non-zero exit also prints a learner-facing message on stdout; still echo it.

## Data Files (debugging reference)

Under `$NANOBOT_READ_DATA_DIR` (default `/root/.nanobot/workspace/memory/`):

| File | Purpose | Owner |
|---|---|---|
| `readings.md` | Source entries (Complete + Polished Version text) | `english-train` writes, `english-read` reads |
| `readings-state.json` | Per-entry Leitner state (`box`, `due`) | `english-read` |
| `read-state.json` | Last push batch + confirmation flag | `english-read` |
| `HISTORY.md` | Shared audit log | Both skills append |

## Leitner Model (for reference)

- 5 active boxes with intervals 1 / 3 / 7 / 14 / 30 days. Box 6 = graduated (never picked again).
- New entry → `box:1, due:today`. Each confirmed push → `box++, due = today + INTERVALS[box]`.
- Daily cap = 3 entries. Ranking: higher box first, oldest-due first within the same box — protects near-graduation items from starvation when low-box entries pile up.
- Graduation path: 5 confirmations over ~54 days. `english-train` must retain entries at least 60 days so Box 5 items don't TTL-out before graduating.
