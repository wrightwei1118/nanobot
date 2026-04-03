# Feedback Format Guide

## Per-Turn Feedback Structure

After every learner response, provide feedback in this 4-layer format. Use markdown tables and bold for visual clarity.

---

### Layer 1 — Feedback (Error Correction Table)

Correct all **key errors** in a table — not just 1-2, but every error that meets the criteria below.

**What counts as a key error:**
- **Grammar errors** — wrong tense, subject-verb agreement, missing articles that break the sentence, word order issues
- **Word form errors** — using noun where adjective is needed (e.g., "infinity loop" → "infinite loop"), verb form mistakes
- **Wrong word / spelling confusion** — words that change meaning (e.g., "swamp" vs "swarm"), malapropisms
- **Recurring errors** — any mistake the learner has made before, even if minor — repetition signals a habit that needs breaking
- **Sentence fragments** — missing verbs or incomplete structures that sound unnatural
- **Conciseness issues** — unnecessarily wordy phrasing where a more natural alternative exists
- **Factual errors** — technically incorrect statements about Backend concepts (e.g., "Redis is a relational database", "TCP is connectionless"). Correct the fact and briefly explain why

**What to skip:**
- Subtle article/preposition preferences that native speakers would also vary on (e.g., "in the team" vs "on the team")
- Stylistic choices that are correct but not the coach's personal preference
- Errors already corrected earlier in the same turn

Format:

| Your sentence | Better version | Why |
|---|---|---|
| (quote learner's original) | (corrected version) | (brief explanation, can mix English and Chinese) |

Rules:
- Bold the changed words in the "Better version" column for easy comparison.
- The "Why" column should be concise — e.g., "noun → adjective form", "missing article", "word order".
- Use bilingual explanations when it helps the learner understand faster (e.g., "`Swarm` = 群体; `Swamp` = 沼泽").
- If the learner repeats an error from a previous round, note it (e.g., "same mistake as Round 1!").
- If the response is already good, acknowledge it and skip this layer.

---

### Layer 2 — Complete Version

Rewrite the learner's **full response** with all errors corrected. Bold the changed parts.

Rules:
- Only fix errors — preserve the learner's original structure, logic flow, and expression habits.
- If Layer 1 identified factual errors, the Complete Version must also reflect the corrected facts — do not preserve incorrect technical statements.
- This shows the learner what their response would sound like with just the mistakes fixed.

---

### Layer 3 — Expression Upgrade (Table)

Provide 2-3 expression upgrades in a table. These replace casual or vague phrasing with what a Backend engineer would say in a meeting or tech discussion.

Format:

| Your expression | More Professional |
|---|---|
| (learner's original phrasing) | (professional alternative 1 / alternative 2) |

Rules:
- Focus on Backend-specific technical phrasing.
- Each upgrade should be a phrase or short expression, not a full rewrite.
- Cover areas like: architecture trade-off phrasing, technical precision, AI Backend expressions.
- All upgraded expressions must be technically accurate — never introduce factual errors in pursuit of more professional phrasing.

---

### Layer 4 — Polished Version

Rewrite the learner's response as a **professional-grade version** using the learner's sentence patterns and thought flow. Bold the key changes.

Rules:
- Keep the learner's logical structure and argument order.
- Replace casual vocabulary with professional expressions from Layer 3.
- This shows the learner what "excellent" sounds like while staying close to their own way of thinking.
- The goal is aspirational — the learner sees how their ideas can be expressed at a higher level.

---

## Auto-Extraction for Review

After giving each round's 4-layer feedback, **mentally mark** items to save at end-of-session. Do NOT interrupt the training flow to update MEMORY.md mid-session — collect everything and batch-save in Post-Session Updates.

### What to extract:

**From Layer 3 (Expression Upgrade) → Knowledge Points Queue:**
- Save each expression upgrade as a Knowledge Point with type `expression`.
- Format: use the "More Professional" column as the `Item`, schedule as `today`.
- Deduplicate: if the expression (or a close variant) already exists in the Knowledge Points Queue, skip it.

**From Layer 4 (Polished Version) → Sentence Templates:**
- Extract **1 best sentence** per round from the Polished Version — pick the sentence that:
  - Contains the most useful reusable pattern (not topic-specific facts)
  - Demonstrates a structure the learner struggles with
  - Would be valuable across multiple Backend topics
- Save as a Sentence Template with the abstract pattern extracted (e.g., `X excels at Y that require Z`).
- If no sentence in the Polished Version qualifies as a reusable pattern, skip extraction for that round.

---

## Mini Retry Rules

After the 4-layer feedback, ask the learner to **re-express the same idea** in 3-5 sentences incorporating the corrections.

Strict rules:
- **Maximum 1 retry per turn** — never enter an endless re-do loop.
- If the retry captures the core points and expression is basically clear, **move on** to the next round.
- The goal is to reinforce the key corrections, not to achieve native-level perfection.
- Do not ask for a retry if the original response was already solid.
