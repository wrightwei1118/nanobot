---
name: english-drill
description: "Sentence template drill practice for Backend English muscle memory. Trigger: say '开始句型练习', 'drill templates', '练习模板'. Runs recall, rewrite, and apply exercises on stored sentence templates."
---

# English Drill — Sentence Template Practice

You run structured drill sessions to help the learner internalize Backend English sentence templates through repetition and rewriting. The goal is building muscle memory for professional sentence patterns.

## When This Skill Activates

- The learner says "开始句型练习", "drill templates", or "练习模板".

## Before Starting

1. Read `memory/MEMORY.md` and locate the **Sentence Templates** section.
2. If no templates exist, tell the learner to add some first via `english-vocab` (e.g., submit a sentence and say "模板").
3. Select **2 templates** for this session, prioritizing:
   - `today` schedule first
   - `review` schedule second
   - Least recently practiced templates

## Session Structure

For each of the 2 selected templates, run 3 exercises in order:

### Exercise 1: Recall

- Show the learner a **hint**: the abstract pattern (e.g., "X offers/provides Y for Z") or 1-2 keywords from the original sentence.
- Ask the learner to **reproduce the full sentence from memory**.
- See `references/drill-format.md` for feedback format.

### Exercise 2: Rewrite

- Show the learner the **original sentence**.
- Ask them to **rewrite it using different words or structure** while keeping the same meaning.
- Encourage: synonym swaps, voice changes (active↔passive), clause reordering.
- See `references/drill-format.md` for feedback format.

### Exercise 3: Apply

- Give the learner a **new Backend scenario** (different from the original context).
- Ask them to **use the same sentence pattern** to describe the new scenario.
- The scenario should be realistic and relevant to Backend engineering.
- See `references/drill-format.md` for feedback format.

## Session Flow

```
Template 1 → Recall → Rewrite → Apply
Template 2 → Recall → Rewrite → Apply
Summary
```

## End-of-Session

After all exercises are complete:

1. **Summary**: report how many templates were practiced and accuracy (e.g., "2 templates, 5/6 exercises correct").
2. **Update MEMORY.md**:
   - Move practiced templates to `review` schedule.
   - Set next review date (3 days from now for first review, 7 days for subsequent).
3. **Log to HISTORY.md**:
   ```
   [YYYY-MM-DD HH:MM] english-drill | Templates practiced: N | Accuracy: X/Y
   ```
