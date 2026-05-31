# Topic Context Index

> **New:** `category:` is now required in group frontmatter; per-`applies_to` overrides are supported via the mapping form.

This index maps **today's topic** (the exact string stored in `MEMORY.md` Current Topic / Preferred Topics) to a topic-specific context file.

## How to use

In `english-train` SKILL.md → **Before Starting**:

1. After today's topic string is decided, look it up in this index (case-insensitive, whitespace-trimmed exact match).
2. If a match exists, read the linked context file **before Round 1**. Treat it as **ground truth** when judging the learner's technical claims.
3. When a misstatement matches an entry in the file's "Common misconceptions" section, quote the correct claim back to the learner.
4. If no entry matches today's topic, proceed without topic-specific context (general Backend knowledge only).

## Mappings

### Group: correlation-request-search-id

| Today's topic (exact match) | Context file |
|---|---|
| `correlation_id propagation in microservices` | [correlation-request-search-id.md](correlation-request-search-id.md) |
| `request_id as a stable cross-service identifier` | [correlation-request-search-id.md](correlation-request-search-id.md) |
| `search_id as a content-addressed cache key` | [correlation-request-search-id.md](correlation-request-search-id.md) |
| `request_id vs correlation_id vs search_id: trade-offs and when to separate them` | [correlation-request-search-id.md](correlation-request-search-id.md) |

<!-- Add new groups below as more topics gain dedicated rubrics. -->
