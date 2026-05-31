# Session Categories

`concept-explanation` is the **default category** — used whenever the session topic (the exact topic string stored in `MEMORY.md`) does not specify a category or the learner's goal is to explain a single concept from scratch.

This file is the **single source of truth** for category definitions and round structures. SKILL.md links here and does not duplicate these rows.

---

## concept-explanation

5 rounds. Use when the learner needs to explain what something is, how it works, and when to apply it.

| Round | Goal | Semantic mode |
|---|---|---|
| R1 | Warm-up — recall the topic name and give a one-sentence summary | definition |
| R2 | Core explanation — explain what it is and how it works | definition |
| R3 | Implementation — describe how it is built and what each piece does internally | causal |
| R4 | Trade-offs — articulate costs, limitations, and alternatives | contrast |
| R5 | When-to-use + Wrap-up — state the conditions under which this is the right choice | conditional / decision |

---

## comparison

5 rounds. Use when the topic names two or more items and the goal is to distinguish and choose between them.

| Round | Goal | Semantic mode |
|---|---|---|
| R1 | Quick recall — name each item and give a one-sentence description of each | definition |
| R2 | Key differences — state the primary axes on which the items differ | contrast |
| R3 | Trade-off matrix — compare items across multiple dimensions (performance, consistency, ops cost, etc.) | contrast |
| R4 | Decision framework — articulate when to pick which option and why | conditional / decision |
| R5 | Wrap-up + personal preference — summarise and state which the learner would choose in a given context | conditional / decision |

---

## troubleshooting

4 rounds. Use when the topic is a failure mode, incident type, or operational problem the learner must diagnose and fix.

| Round | Goal | Semantic mode |
|---|---|---|
| R1 | Symptoms — describe what the user observes or what alerts fire | definition |
| R2 | Diagnosis — explain how to localise the root cause from the symptoms | causal |
| R3 | Fix — describe the actual remediation steps | conditional |
| R4 | Post-mortem — state the root cause and how to prevent recurrence | causal |

---

## system-design

6 rounds. Use when the topic asks the learner to design a system or sub-system from scratch.

| Round | Goal | Semantic mode |
|---|---|---|
| R1 | Requirements + scope — clarify functional / non-functional requirements and set boundaries | definition |
| R2 | High-level architecture — sketch the major components and their interactions | definition |
| R3 | Data model + APIs — specify key data structures, schemas, and interface contracts | definition |
| R4 | Scaling + bottlenecks — identify where the design breaks under load and how to address it | causal |
| R5 | Trade-offs + alternatives — compare design choices and explain why one was selected | contrast |
| R6 | Wrap-up — summarise the design and state what you would revisit first | conditional / decision |
