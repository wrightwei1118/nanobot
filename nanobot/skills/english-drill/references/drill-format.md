# Drill Exercise Format Guide

## Exercise 1: Recall — Feedback Format

After the learner attempts to reproduce the sentence from memory:

```
Accuracy: ✅ Correct / ⚠️ Partial / ❌ Incorrect

Your version:
(Quote the learner's attempt)

Original:
(Show the original sentence)

[If errors exist]
Key differences:
- (Point out specific words or structures that were wrong or missing)
```

Rules:
- Accept minor word order variations if the meaning is preserved.
- Flag missing key terms that change the meaning.
- If the learner's version is a valid alternative phrasing, mark it as correct and note the difference.

## Exercise 2: Rewrite — Feedback Format

After the learner rewrites the sentence:

```
Rewrite quality: ⭐⭐⭐ (1-3 stars)

Your rewrite:
(Quote the learner's rewrite)

Assessment:
- Meaning preserved: Yes / Partially / No
- Natural sounding: Yes / Somewhat / No
- Structural change: Yes / Minimal / None (just synonym swap)

[If the rewrite is valid but limited]
Additional variations you could try:
- (Suggest 1-2 more rewrites the learner hasn't tried)

[If the rewrite changes meaning]
Meaning shift:
- Your version implies: (what their version means)
- Original means: (what the original means)
- Suggested fix: (how to adjust)
```

Rules:
- A pure synonym swap (e.g., "offers" → "provides") gets 1 star — push for structural changes.
- A structural rearrangement with preserved meaning gets 2-3 stars.
- Compare against the known variations stored in MEMORY.md, but also accept novel valid rewrites.

## Exercise 3: Apply — Feedback Format

After the learner applies the pattern to a new scenario:

```
Application: ✅ Pattern correctly applied / ⚠️ Partially applied / ❌ Pattern not used

Your sentence:
(Quote the learner's sentence)

Pattern check:
- Pattern used: [the abstract pattern, e.g., "X offers/provides Y for Z"]
- Context fit: Does the sentence make sense for the given scenario? Yes / No
- Technical accuracy: Is the Backend content correct? Yes / No

[If the pattern wasn't applied correctly]
Example using the pattern:
(Show how the pattern could be applied to this scenario)
```

Rules:
- The learner doesn't need to use the exact same words — the pattern structure matters.
- If they produce a valid sentence but don't use the target pattern, point this out and ask for a retry.
- If the Backend content is technically wrong, correct it separately from the pattern feedback.

## Scenario Generation Guidelines

When creating Apply scenarios, choose from these Backend contexts:
- System design discussions (scaling, caching, load balancing)
- Code review conversations (suggesting improvements, explaining trade-offs)
- Incident response (describing what happened, proposing fixes)
- Architecture decisions (comparing approaches, justifying choices)
- Team communication (status updates, technical proposals)

Keep scenarios concrete and specific — "Your team is debating whether to use Redis or Memcached for session caching" is better than "Talk about caching."
