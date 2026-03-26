---
name: english-vocab
description: "Process English vocabulary, expressions, Backend terminology, sentence templates, and speaking topics submitted by the learner. Trigger: when the user sends new words, unfamiliar sentence patterns, Backend terms, technical expressions, sentence templates, or topics they want to practice."
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
Classify as: word / phrase / sentence pattern / technical term / Backend idiom / **topic** / **sentence template**

If the input is a **topic** (a Backend concept or scenario the learner wants to practice discussing), skip to the topic handling flow below.

If the input is a **sentence template** (a complete sentence the learner wants to internalize as a reusable pattern, or they explicitly say "模板"/"template"), skip to the sentence template handling flow below.

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

### Comparison Topic Detection

If the topic contains a comparison pattern (A vs B, A vs B vs C, A 和 B 的区别, etc.), **split it by default** into independent sub-topics plus a final comparison summary:

**Example**: learner submits "gRPC vs REST vs GraphQL"
→ Split into:
1. `REST API design` — pending
2. `gRPC fundamentals` — pending
3. `GraphQL basics` — pending
4. `REST vs gRPC vs GraphQL: comparison and trade-offs` — pending (summary)

**Rules**:
- Each sub-topic focuses on explaining that one technology/concept independently (what it is, how it works, when to use it).
- The final summary topic focuses purely on **comparing** the items: differences, trade-offs, and when to pick each.
- All sub-topics share the same `group` tag so `english-train` trains them in order.
- The summary topic is always last in the group.

Add to Preferred Topics with `Group` column:
```
| Topic | Added | Status | Group |
| REST API design | 2024-01-15 | pending | grpc-rest-graphql |
| gRPC fundamentals | 2024-01-15 | pending | grpc-rest-graphql |
| GraphQL basics | 2024-01-15 | pending | grpc-rest-graphql |
| REST vs gRPC vs GraphQL: comparison and trade-offs | 2024-01-15 | pending | grpc-rest-graphql (summary) |
```

**Acknowledge** — tell the learner you split the comparison into N+1 sessions (N individual + 1 summary), and list them.

### Regular (Non-Comparison) Topics

1. **Acknowledge** — confirm the topic has been added.
2. **Add to Preferred Topics** in MEMORY.md under `### Preferred Topics`:
   ```
   | Topic | Added | Status | Group |
   | circuit breaker pattern | 2024-01-15 | pending | — |
   ```
3. **Status values**: `pending` (not yet trained), `in_progress` (currently being trained), `done` (completed).
4. Topics here are **prioritized over** the general topic pool in `english-train`.

Log to HISTORY.md:
```
[YYYY-MM-DD HH:MM] english-vocab | Topic added: [topic name]
```
For comparison topics:
```
[YYYY-MM-DD HH:MM] english-vocab | Comparison topic split: [original] → [sub-topic 1], [sub-topic 2], ..., [summary topic]
```

## Sentence Template Handling

When the learner submits a complete sentence that looks like a reusable professional pattern (or explicitly says "模板"/"template"):

### Detection

A sentence template is a complete sentence that:
- Expresses a reusable Backend communication pattern (e.g., explaining trade-offs, proposing solutions, describing architecture)
- Contains substitutable slots — parts that can be swapped for different contexts
- Is distinct from a simple phrase or idiom: it's a full sentence structure the learner wants to internalize

### Processing

1. **Identify the core pattern** — extract the abstract structure:
   - e.g., "The Graph pattern offers greater flexibility for complex workflows" → `X offers/provides [greater/more] Y for Z`

2. **Provide 2-3 rewrite variations** — synonym swaps, structural rearrangements:
   - Verb swaps: offers → provides, gives, enables
   - Adjective swaps: greater → more, improved, enhanced
   - Structural: active → passive voice, clause reordering
   - e.g., "provides more flexibility" / "gives you more flexibility" / "enables greater flexibility in complex workflows"

3. **Note key substitutable slots** — which parts are interchangeable and what kinds of substitutions work

### Storage

Add to the **Knowledge Points Queue** in MEMORY.md with type `sentence template`:

```
| Item | Type | Priority | Schedule | Added |
| The Graph pattern offers greater flexibility for complex workflows | sentence template | high | today | 2026-03-26 |
```

Add to a new **Sentence Templates** section in MEMORY.md (create if it doesn't exist):

```
| # | Original | Variations | Pattern | Schedule | Added |
| 1 | The Graph pattern offers greater flexibility for complex workflows | provides more flexibility / gives you more flexibility / enables greater flexibility | X offers/provides Y for Z | today | 2026-03-26 |
```

### Logging

Append to `memory/HISTORY.md`:
```
[YYYY-MM-DD HH:MM] english-vocab | Template added: [original sentence] (N variations)
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
