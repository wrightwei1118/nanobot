---
name: english-read
description: "Daily read-aloud practice using corrected and polished versions from past training sessions. Trigger: say '朗读练习', 'read aloud', or '开始朗读'. Picks 3 entries by spaced repetition intervals and presents them for reading — no feedback, just material."
---

# English Read — Daily Read-Aloud Practice

You provide read-aloud material drawn from the learner's past `english-train` sessions. The goal is building pronunciation fluency, intonation, and muscle memory for professional Backend English. You do NOT give feedback — just present the text.

## When This Skill Activates

- The learner says "朗读练习", "read aloud", or "开始朗读".

## Before Starting

1. Read `memory/readings.md` — this contains Complete Versions and Polished Versions saved from past `english-train` sessions.
2. If the file is empty or doesn't exist, tell the learner to run a few `english-train` sessions first to generate material.

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

Append to `memory/HISTORY.md`:
```
[YYYY-MM-DD HH:MM] english-read | Entries read: 3 | Dates: [date1], [date2], [date3]
```
