---
name: english-read
description: "Daily read-aloud practice using corrected and polished versions from past training sessions. Trigger: say '朗读练习', 'read aloud', or '开始朗读'. Also handles confirmation: '收到', '已读', 'done', 'got it'. Picks 3 entries by spaced repetition intervals and presents them for reading — no feedback, just material."
---

# English Read — Daily Read-Aloud Practice

You provide read-aloud material drawn from the learner's past `english-train` sessions. The goal is building pronunciation fluency, intonation, and muscle memory for professional Backend English. You do NOT give feedback — just present the text.

## When This Skill Activates

- The learner says "朗读练习", "read aloud", or "开始朗读" → **read-aloud session**.
- Triggered by the daily cron job `daily-english-read` → **read-aloud session**.
- The learner says "收到", "已读", "done", or "got it" → **confirmation only** (see Confirmation Flow below).

## Before Starting

1. **Auto-register cron job** — call `cron(action="list")` and check if a job named `daily-english-read` exists.
   - If **not found**: call `cron(action="add", name="daily-english-read", message="朗读练习", cron_expr="0 6 * * *", tz="Asia/Shanghai")` to register daily read-aloud (every day 06:00 Beijing time).
   - If **found**: skip.
2. Read `memory/readings.md` — this contains Complete Versions and Polished Versions saved from past `english-train` sessions.
3. If the file is empty or doesn't exist, tell the learner to run a few `english-train` sessions first to generate material.

## Confirmation Flow

This skill tracks push/confirmation state in `memory/read-state.json`:

```json
{
  "last_push_date": "2026-04-11",
  "last_push_entries": [
    {"date": "2026-04-10", "topic": "API Design", "round": 3},
    {"date": "2026-04-07", "topic": "Code Review", "round": 2},
    {"date": "2026-04-02", "topic": "Deployment", "round": 5}
  ],
  "confirmed": false
}
```

### On confirmation trigger ("收到" / "已读" / "done" / "got it")

1. Read `memory/read-state.json`.
2. Set `confirmed` to `true` and save.
3. Reply: "已确认，明天会推送新内容。"
4. Done — do NOT start a read-aloud session.

### On read-aloud session (manual or cron)

Before selecting entries, read `memory/read-state.json`:

- **If file exists AND `confirmed == false`**:
  - **If triggered by cron**: re-push the **same entries** listed in `last_push_entries`. Look them up in `memory/readings.md` by date + topic. Prepend a reminder: "上次推送的内容还没确认，再来一遍 👇". After presenting, keep `confirmed: false` (still waiting for confirmation).
  - **If triggered manually** (learner said "朗读练习"): treat as implicit confirmation of the previous push — set `confirmed: true`, then proceed to select **new** entries normally.
- **If file doesn't exist OR `confirmed == true`**: select new entries normally (see Selection below).

## Selection: Pick 3 Entries

Select **3 entries** from `memory/readings.md` using spaced repetition intervals:

| # | Time range | Purpose |
|---|---|---|
| 1 | Yesterday or today | Fresh content, first reinforcement |
| 2 | 3-5 days ago | Medium-term consolidation |
| 3 | 7+ days ago | Long-term retention |

**Fallback rules:**
- If a time range has no entries, expand to the nearest available range.
- If total entries < 3, use whatever is available.
- Within a time range, prefer entries from topics where the learner had more corrections (more errors = more to internalize).
- Never pick the same entry twice in one session.

## Session Format

Present the 3 entries in order. For each entry:

```
### [N/3] — [Topic] (Round [R], [date])

**Complete Version (read aloud first):**
[text]

**Polished Version (then read this):**
[text]
```

Rules:
- No feedback, no corrections, no commentary between entries.
- After presenting all 3, end with a brief closing: "Done! [N] entries read today."
- The learner reads at their own pace — do not rush or prompt them to continue.

## Post-Session

1. Write `memory/read-state.json` with the entries just presented and `confirmed: false`.
2. Append to `memory/HISTORY.md`:
```
[YYYY-MM-DD HH:MM] english-read | Entries read: 3 | Dates: [date1], [date2], [date3]
```
