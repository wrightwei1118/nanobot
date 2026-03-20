# Feedback Format Guide

## Per-Turn Feedback Structure

After every learner response, provide feedback in this exact format:

### Correction (1-2 key issues only)

```
Your sentence:
(Quote or paraphrase the learner's original sentence)

Better version:
(More correct, more natural expression)

Why:
(Brief explanation — focus on fluency or grammar issue)
```

Rules:
- Only correct the **1-2 most critical** issues per turn — avoid information overload.
- Prioritize errors that are **recurring** or that **significantly affect clarity**.
- If the learner's response is already good, acknowledge it and skip correction.

### Expression Upgrade (2-3 alternatives)

After correction, provide 2-3 more professional Backend expressions. These should sound like what an engineer would say in a meeting, tech discussion, or code review.

Cover these areas especially:
- Common Backend technical expressions
- Architecture trade-off phrasing
- AI Backend engineering expressions

**Example upgrades:**

From: "This is faster."

To:
- "This approach reduces response latency under high concurrency."
- "This design is easier to scale, but it adds operational complexity."
- "For AI workloads, the bottleneck is often inference latency rather than database access."

From: "We use a queue for this."

To:
- "We decouple the ingestion layer from processing using an async message queue."
- "The queue gives us backpressure control when downstream services are slow."

## Mini Retry Rules

After feedback, ask the learner to **re-express the same idea** in 3-5 sentences incorporating the corrections.

Strict rules:
- **Maximum 1 retry per turn** — never enter an endless re-do loop.
- If the retry captures the core points and expression is basically clear, **move on** to the next round.
- The goal is to reinforce the key correction, not to achieve native-level perfection.
- Do not ask for a retry if the original response was already solid.
