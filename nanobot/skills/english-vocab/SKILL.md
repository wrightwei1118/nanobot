---
name: english-vocab
description: "Process English vocabulary, expressions, Backend terminology, and speaking topics submitted by the learner. Trigger: when the user sends new words, unfamiliar sentence patterns, Backend terms, technical expressions, or topics they want to practice."
---

# English Vocab — Vocabulary and Learner Profile Management

You handle all vocabulary, expression, and terminology inputs from the learner. You also own the learner profile — assessing level, tracking weaknesses, and maintaining the knowledge points queue.

## When This Skill Activates

- The learner sends a new word, phrase, sentence pattern, or Backend term.
- The learner asks about an unfamiliar expression or technical concept.
- The learner is in week 1 assessment phase and submitting materials for evaluation.

## Processing New Knowledge Points

When the learner submits new content:

### 1. Identify Type
Classify as: word / phrase / sentence pattern / technical term / Backend idiom / **topic**

If the input is a **topic** (a Backend concept or scenario the learner wants to practice discussing), skip to the topic handling flow below.

### 2. Provide Immediate Feedback
- **Meaning**: clear, concise explanation
- **Backend example sentence**: show how it's used in a real Backend technical discussion
- **Common collocations**: related expressions or typical pairings

Example:
> **"backpressure"**
> - Meaning: a mechanism where a downstream system signals upstream to slow down when it can't keep up.
> - Backend example: "We added backpressure handling to the message queue consumer so it stops pulling when the processing pipeline is saturated."
> - Collocations: "apply backpressure", "backpressure-aware consumer", "propagate backpressure upstream"

### 3. Assess Priority
Consider:
- How relevant is this to the learner's current weaknesses (check Learner Profile)?
- Does it connect to an upcoming or recent training topic?
- Is it a high-frequency Backend expression the learner will need repeatedly?

### 4. Schedule
Assign one of:
- `today` — integrate into the next training session
- `queued` — add to the training plan for a future session
- `review` — already seen before; schedule for reinforcement

### 5. Update MEMORY.md
Add the item to the **Knowledge Points Queue** table:

```
| Item | Type | Priority | Schedule | Added |
| backpressure | technical term | high | today | 2024-01-15 |
```

## Topic Handling

When the learner submits a topic they want to practice (e.g., "I want to practice talking about circuit breakers" or "加一个话题：gRPC vs REST"):

1. **Acknowledge** — confirm the topic has been added.
2. **Add to Preferred Topics** in MEMORY.md under `### Preferred Topics`:
   ```
   | Topic | Added | Status |
   | circuit breaker pattern | 2024-01-15 | pending |
   ```
3. **Status values**: `pending` (not yet trained), `in_progress` (currently being trained), `done` (completed).
4. Topics here are **prioritized over** the general topic pool in `english-train`.

Log to HISTORY.md:
```
[YYYY-MM-DD HH:MM] english-vocab | Topic added: [topic name]
```

## Week 1: Assessment Mode

During the first week (`training_day_counter` <= 7 in MEMORY.md), the primary goal is **assessment over training**.

From the learner's submissions and any lightweight trial sessions, build the Learner Profile by inferring:

1. **Current English proficiency level**
2. **Vocabulary gaps** — which technical or general words they lack
3. **Grammar weaknesses** — patterns of errors (tense, articles, structure)
4. **Fluency barriers** — where they get stuck, filler words, inability to transition
5. **Backend communication gaps** — which technical concepts they cannot articulate

See `references/learner-profile-guide.md` for the full profile format and assessment methodology.

### What to Track from Week 1

- Can the learner explain basic technical concepts?
- What are their most common grammar mistakes?
- Where do they get stuck in technical discussions?
- What topic depth can they handle comfortably?

All of this feeds into the Learner Profile stored in MEMORY.md.

## Learner Profile Management

The profile lives in `memory/MEMORY.md` under `## English Speaking Coach > ### Learner Profile`.

### Update Rules
- Update after every vocab submission batch that reveals new patterns.
- Be specific — never write "needs improvement"; always cite concrete examples.
- When a weakness improves, note the improvement or remove the entry.
- List the most impactful weakness first in each category.

See `references/learner-profile-guide.md` for the complete format and detailed rules.

## Post-Update Logging

After processing vocabulary, append to `memory/HISTORY.md`:
```
[YYYY-MM-DD HH:MM] english-vocab | Added: [item list] | Types: [types] | Schedule: [today/queued/review]
```
