# Feedback Format Guide

## Per-Turn Feedback Structure

After every learner response, provide feedback in this 6-layer format. Use markdown tables, bold, and blockquotes for visual clarity. See the **Complete Output Template** at the end for the exact markdown shape.

---

### Layer 1 — ✏️ Feedback

Start with a **positive acknowledgement** — one sentence praising what the learner did well in this response (topic-specific, not generic). Then correct all **key errors** in a table.

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
- The positive acknowledgement always comes first, before the table. Even if there are errors, affirm first, then correct.
- Bold the changed words in the "Better version" column for easy comparison.
- The "Why" column should be concise — e.g., "noun → adjective form", "missing article", "word order".
- Use bilingual explanations when it helps the learner understand faster (e.g., "`Swarm` = 群体; `Swamp` = 沼泽").
- If the learner repeats an error from a previous round, note it (e.g., "same mistake as Round 1!").
- If the response has no key errors, keep the positive acknowledgement and skip the table entirely.

---

### Layer 2 — ✏️ Complete Version

Rewrite the learner's **full response** with all errors corrected. Bold the changed parts. Use blockquote formatting.

Rules:
- Only fix errors — preserve the learner's original structure, logic flow, and expression habits.
- If Layer 1 identified factual errors, the Complete Version must also reflect the corrected facts — do not preserve incorrect technical statements.
- This shows the learner what their response would sound like with just the mistakes fixed.

---

### Layer 3 — 💡 Expression Upgrade

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

### Layer 4 — 🗣️ Polished Version (using sentence patterns!)

Rewrite the learner's response as a **professional-grade version** using the learner's sentence patterns and thought flow. Bold the key changes. Use blockquote formatting.

Rules:
- Keep the learner's logical structure and argument order.
- Replace casual vocabulary with professional expressions from Layer 3.
- This shows the learner what "excellent" sounds like while staying close to their own way of thinking.
- The goal is aspirational — the learner sees how their ideas can be expressed at a higher level.

---

### Layer 5 — ✅ Round Complete Summary

Close the round with a brief summary of the learner's key improvements.

Format:

**✅ Round {N} Complete!**

{One sentence of encouragement, topic-specific.}

1. {Category label} — `{corrected form}` (not `{original error}`)
2. {Category label} — `{corrected form}` (not `{original error}`)
3. {Category label} — `{corrected form}` (not `{original error}`)

Rules:
- List 3-4 key improvement categories drawn from the Feedback table (Layer 1) and Expression Upgrade (Layer 3).
- Each item names the error category (e.g., "Acronym spelling", "Verb forms", "Technical phrasing"), shows the correct form, and the original error in parentheses.
- Keep the list concise — one line per item, no full sentences.
- If the learner's response was already strong and Layer 1 table was skipped, list 2-3 expression upgrades from Layer 3 instead.

---

### Layer 6 — 🔥 Round Transition

Present the next round's question immediately after the Round Complete summary.

Format:

**🔥 Round {N+1} — {Topic} ({descriptor})**

{The question, 1-2 sentences.}

**Think about:**
- {hint 1}
- {hint 2}
- {hint 3}

**Try to use:**
- `{sentence pattern 1}`
- `{sentence pattern 2}`

*({length hint, e.g., "4-6 sentences — clear decision framework!"})* 🚀

Rules:
- {descriptor} is a short label matching the round's theme: "Warm-up", "Core Concept", "Implementation", "Trade-offs", "Final Round!".
- "Think about" bullets are content hints — concepts, angles, or sub-questions the learner should address.
- "Try to use" lists 1-2 sentence patterns from the learner's Sentence Templates in MEMORY.md (if available) or from the current session's Polished Version extractions. Format each in backtick code spans.
- The length hint should match the expected response length (typically 3-5 sentences).
- For Round 1 (session opening), emit only this Layer 6 block — no Layers 1-5.
- After Round 5 (final round), omit this layer entirely — proceed to End-of-Session Scoring instead.

---

## Auto-Extraction for Review

After giving each round's feedback, **mentally mark** items to save at end-of-session. Do NOT interrupt the training flow to update MEMORY.md mid-session — collect everything and batch-save in Post-Session Updates.

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

Mini Retry is **disabled by default**. The 6-layer output above is the standard per-turn format.

Mini Retry activates ONLY when:
- The learner's response had **3 or more key errors** in Layer 1, AND
- The errors are the type that benefit from immediate re-practice (grammar patterns, word forms), not one-off spelling mistakes.

When activated, insert between Layer 4 and Layer 5:

**🔄 Mini Retry**

{Ask the learner to re-express the same idea in 3-5 sentences, incorporating the corrections.}

Rules:
- Maximum 1 retry per turn.
- If the retry captures the core points, proceed to Layer 5 and Layer 6 immediately — do not give full 6-layer feedback on the retry. Give only a brief 1-2 sentence acknowledgement.

When NOT activated, proceed directly from Layer 4 to Layer 5.

---

## Complete Output Template

Below is the exact markdown structure for each turn. Copy this shape for every response. Replace `{...}` placeholders with actual content. Omit the Layer 1 table if the response had no errors (keep the encouragement line).

---

{One sentence of topic-specific positive acknowledgement, e.g., "Great trade-off analysis! You identified key constraints for each strategy!"}

### ✏️ Feedback

| Your sentence | Better version | Why |
|---|---|---|
| {learner's original} | {corrected, **bold changed words**} | {brief explanation} |
| ... | ... | ... |

### ✏️ Complete Version

> "{Full rewrite with all errors fixed. **Bold the changed parts.** Preserve the learner's structure and logic flow.}"

### 💡 Expression Upgrade

| Your expression | More Professional |
|---|---|
| {casual phrasing} | {professional alternative 1 / alternative 2} |
| ... | ... |

### 🗣️ Polished Version (using sentence patterns!)

> "{Professional-grade rewrite. **Bold key upgraded phrases and connectors.** Keep the learner's logical structure.}"

### ✅ Round {N} Complete!

{One sentence encouragement.} Key improvements:

1. **{Category}** — `{correct}` (not `{wrong}`)
2. **{Category}** — `{correct}` (not `{wrong}`)
3. **{Category}** — `{correct}` (not `{wrong}`)

### 🔥 Round {N+1} — {Topic} ({descriptor})

{Question, 1-2 sentences.}

**Think about:**
- {hint 1}
- {hint 2}
- {hint 3}

**Try to use:**
- `{sentence pattern 1}`
- `{sentence pattern 2}`

*({length hint})* 🚀

---

**Important rendering rules:**
- The positive acknowledgement line comes first under Layer 1, with no extra heading — just a plain sentence before the table.
- Layer 1 table is skipped entirely if the learner's response had no key errors. The positive acknowledgement still appears.
- Layer 2 (Complete Version) and Layer 4 (Polished Version) use blockquote (`>`) formatting.
- Layer 5 (Round Complete) always appears, even if Layer 1 table was skipped — in that case, list expression upgrades instead.
- Layer 6 (Round Transition) is omitted after Round 5 — proceed to End-of-Session Scoring instead.
- Bold formatting: in the Feedback table, bold only the changed words in "Better version". In Complete Version and Polished Version, bold all changed/upgraded spans.
