---
name: english-review
description: "Weekly review of Backend English speaking training progress. Trigger: say '本周复盘', 'weekly review', or runs automatically after every 7 training sessions. Generates a progress report with score trends, grammar patterns, and next-week plan."
---

# English Review — Weekly Progress Review

You generate a comprehensive weekly review of the learner's Backend English speaking training progress. This review analyzes trends, identifies patterns, and sets the plan for the next week.

## When This Skill Activates

- The learner says "本周复盘" or "weekly review."
- 7 or more calendar days have passed since `last_review_date` in MEMORY.md.

## Data Collection

Before generating the report, gather all necessary data:

1. **From `memory/MEMORY.md`**:
   - Score History (recent 14 days)
   - Current Topic status
   - Learner Profile
   - Top Issue Tracker
   - Knowledge Points Queue
   - Training State (`session_counter`, `training_start_date`, `last_review_date`)

2. **From `memory/HISTORY.md`**:
   - Search for all `english-train` entries since the last review date.
   - Search for all `english-vocab` entries since the last review date.
   - Search for all `english-drill` entries since the last review date.

## Analysis Dimensions

Analyze the collected data across these dimensions:

### 1. Topic Fluency Progress
- Which Backend topics does the learner now discuss more fluently?
- Which topics still feel rough or were marked `unfinished`?
- How well did the learner handle AI-era Backend topics vs. traditional ones?

### 2. Score Trends
- Calculate average scores for the week (Fluency, Grammar, Technical Clarity).
- Compare against the previous week's averages.
- Identify upward or downward trends in each dimension.

### 3. Grammar Patterns
- What was the most frequent grammar issue this week?
- Which grammar issues from last week improved?
- Which grammar issues need to carry forward?

### 4. Expression Growth
- Which Backend expressions did the learner successfully use?
- Which expressions are still shaky and need reinforcement?
- How is the learner progressing with AI Backend vocabulary specifically?

### 5. Sentence Template Mastery
- Which templates has the learner internalized (consistently correct in recall + rewrite)?
- Which templates are still shaky (errors in recall, limited rewrite variety)?
- How well does the learner transfer patterns to new contexts (Apply exercise results)?
- Are there enough templates in the queue, or should the learner add more?

### 6. Knowledge Points Status
- Which items from the queue were practiced this week?
- Which items are still queued?
- What new items were added?

## Report Generation

Generate the report following the template in `references/review-template.md`. The report must:

- Be encouraging but honest — highlight real progress without inflating it.
- Always compare against the previous week to show trajectory.
- Include concrete examples from training sessions to support observations.
- Provide actionable recommendations for the next week.

## Scoring Reference

Use the anchor points in `references/scoring.md` when interpreting score trends and assessing whether score changes are meaningful.

## Post-Review Updates to MEMORY.md

After generating the report, update `memory/MEMORY.md`:

1. **Learner Profile**: refresh based on the week's observations. Update weakness descriptions, note improvements, adjust level if warranted.
2. **Knowledge Points Queue**: reset priorities — promote `queued` items that align with next week's topics to `today`; move practiced items to `review` status.
3. **Training State**: update `last_review_date` to today's date. Week number is calculated as `(today - training_start_date).days // 7 + 1` — do not store it separately.
4. **Score History**: archive rows older than 14 calendar days — move them to `memory/HISTORY.md` with a `[YYYY-MM-DD] score-archive` tag.
5. **Top Issue Tracker**: re-evaluate the current top issue based on this week's data. If the issue has improved, promote a new one.

Append the review summary to `memory/HISTORY.md`:
```
[YYYY-MM-DD HH:MM] english-review | Week N (Sessions X-Y) | Avg: F[x] G[x] T[x] | Top improvement: [area] | Focus next week: [topic/grammar point]
```
