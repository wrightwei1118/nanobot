# Anti-Abuse Examples

This document catalogs four canonical bad outputs that violate the Layer 6 / Layer 4 gates defined in [`feedback-format.md`](feedback-format.md). Each example is tagged with a letter (A/B/C/D) and the gate it violates (G1/G2/G3/G4), so readers and lint tooling can reference them by tag.

The literal bad-output snippets are kept **outside** this file — they live as raw fixtures under `tests/fixtures/english-train/anti-abuse/` so that lint scanners over `nanobot/skills/english-train/**/*.md` do not trip on intentionally-malformed content. Each example below points to its fixture file.

> **Gate reference (from `feedback-format.md` Layer 6 rules):**
> - **G1 Round-goal match** — template's semantic mode must match the round's mode in [`topics-context/_categories.md`](topics-context/_categories.md).
> - **G2 Topic-domain match** — template must share ≥1 backend-engineering domain noun with today's topic.
> - **G3 Count cap** — never list more than 2 templates.
> - **G4 Intent preservation** — Layer 4 Polished Version must preserve the learner's propositional content; never bend meaning to fit a template.

---

## Example A (violates G3 — count cap)

**Tag:** A — G3
**Layer:** 6 (Round Transition, `**Try to use:**` block)
**Fixture:** [`tests/fixtures/english-train/anti-abuse/a-stuffing.md`](../../../../tests/fixtures/english-train/anti-abuse/a-stuffing.md)

A Layer 6 emission lists **five** sentence patterns under `**Try to use:**`, well over G3's hard cap of two. This is "pattern stuffing" — the model treats the template list as a recommendation buffet rather than a curated 0-2 item shortlist. Even if every individual pattern cleared G1 and G2, the count alone is a G3 violation.

**How to detect:** count the bullet lines in the `**Try to use:**` block of any Layer 6 output. If `>2`, fail G3.

---

## Example B (violates G1 — round-goal match)

**Tag:** B — G1
**Layer:** 6 (Round Transition, `**Try to use:**` block)
**Topic context:** `request_id propagation in microservices`, **Round 1 (Warm-up)**
**Fixture:** [`tests/fixtures/english-train/anti-abuse/b-mismatch.md`](../../../../tests/fixtures/english-train/anti-abuse/b-mismatch.md)

The fixture proposes a contrast/trade-off pattern (`X excels at Y but Z, whereas A is better at B`) for a **Warm-up** round whose semantic mode is **definition**, not contrast. The pattern is grammatically fine and topically relevant in a later round, but it asks the learner to compare two things before they have even defined one — round-goal mismatch.

**How to detect:** infer the template's mode from its connectives (`whereas`, `but`, `excels at … better at …` → contrast); look up the round's expected mode in `topics-context/_categories.md`; if mismatch, fail G1.

---

## Example C (violates G2 — topic-domain match)

**Tag:** C — G2
**Layer:** 6 (Round Transition, `**Try to use:**` block)
**Topic context:** `LRU cache eviction policies` (any round)
**Fixture:** [`tests/fixtures/english-train/anti-abuse/c-off-topic.md`](../../../../tests/fixtures/english-train/anti-abuse/c-off-topic.md)

The fixture's concrete example (`the alarm fires when p99 latency exceeds the SLO`) lives in the monitoring/alerting domain. The session's topic is caching — domain nouns are `cache`, `eviction`, `LRU`, `hit/miss`, `TTL`, etc. There is **zero overlap** between the template's example nouns and the topic's domain nouns (literally or via morphological variant). G2 requires ≥1 shared backend-engineering domain noun; the fixture has none.

**How to detect:** extract content nouns from the template's example; intersect with the topic string and the matched `topics-context/` entry's `applies_to` keywords; if the intersection is empty, fail G2.

---

## Example D (violates G4 — intent preservation)

**Tag:** D — G4
**Layer:** 4 (Polished Version)
**Fixture:** [`tests/fixtures/english-train/anti-abuse/d-distortion.md`](../../../../tests/fixtures/english-train/anti-abuse/d-distortion.md)

Learner's original intent (paraphrased): "we use `correlation_id` so that logs from one user request can be grepped across services" — a **causal/purpose** statement about a single ID. The Polished Version in the fixture rewrites it as a **contrast** between `correlation_id` and an invented `search_id`, complete with a fabricated claim about content-addressed caching. The rewrite invents a comparison that wasn't in the learner's input, just to fit a contrast template. G4 requires preserving the learner's propositional content (same actors, same claims, same scope); when no template fits without distortion, fall back to a generic professional rewrite.

**How to detect:** compare the actors and claims in the Polished Version against the learner's original. If the Polished Version introduces new actors (e.g., `search_id` was never mentioned) or new claims (e.g., a comparison the learner did not make), fail G4.

---

## Mapping summary

| Letter | Gate | Layer | One-line summary |
|---|---|---|---|
| A | G3 | 6 | Five `**Try to use:**` bullets — count cap is 2. |
| B | G1 | 6 | Contrast template recommended in a Warm-up (definition) round. |
| C | G2 | 6 | Monitoring-domain template recommended for a caching topic. |
| D | G4 | 4 | Polished Version invents a comparison the learner never made. |

---

## For lint implementers (phase 2 — T9 / T11)

The fixture files at `tests/fixtures/english-train/anti-abuse/*.md` contain the literal bad output snippets, with no surrounding commentary. They are intentionally outside the `nanobot/skills/english-train/` tree so that any lint that scans `nanobot/skills/english-train/**/*.md` will **not** flag them during normal CI runs.

When you wire up T9 / T11 lint tests, point the test harness directly at these fixture paths and assert that the linter reports the expected gate violation (A→G3, B→G1, C→G2, D→G4). The fixture file names encode the letter for easy parametrization.

If a future change requires inlining a literal bad block into a doc under `nanobot/skills/english-train/`, wrap it with the marker pattern below and teach the linter to skip text between these markers:

```
<!-- lint-skip-anti-abuse-fixture-start -->
...literal bad block here...
<!-- lint-skip-anti-abuse-fixture-end -->
```

The current design (fixtures-only) avoids needing this marker today.
