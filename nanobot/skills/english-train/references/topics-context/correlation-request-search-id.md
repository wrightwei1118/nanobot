---
group: correlation-request-search-id
category: concept-explanation
applies_to:
  - "correlation_id propagation in microservices"
  - "request_id as a stable cross-service identifier"
  - "search_id as a content-addressed cache key"
  - topic: "request_id vs correlation_id vs search_id: trade-offs and when to separate them"
    category: comparison
---

# Topic Context — correlation_id / request_id / search_id

This file is the **judging rubric** for any topic in the `correlation-request-search-id` group. Use it as ground truth when evaluating the learner's technical claims about these three identifiers.

The rubric is framework- and language-agnostic. The learner is **not** expected to name specific classes, services, or framework components — only to articulate the patterns and trade-offs.

## Key claims (must be true)

### About correlation_id
- It is **caller-controlled**: each gRPC (or HTTP) call carries one in its Context, typically extracted from a `Correlation-ID` header by an inbound interceptor and stored under a dedicated Context key.
- Its value can change **across inbound requests** (e.g. pagination, applying a filter, reranking — each is a new HTTP call to the gateway/BFF and may carry a different correlation_id).
- Within a **single inbound request**, a channel-level gRPC client interceptor can auto-propagate it to all outbound RPCs (so Create and Poll share the same MDC). Whether such an interceptor exists depends on the framework: many Java service frameworks ship one out of the box; many Python services pass the value manually per call site.
- When no auto-interceptor exists, correlation_id is passed manually per call site. This is error-prone — different endpoints can forget to pass it, hard-code an empty string, or pass different values.

### About request_id
- It is a **snapshot** of the correlation_id seen at the moment the cache entry was first created, then frozen — write-once / first-writer-wins.
- It is stored as a field within the per-cycle metadata record (i.e. as the metadata's `correlationId` field).
- The metadata-initialization function writes it **only when no metadata entry exists**. Subsequent calls (Create or Poll for the same cycle) read from cache and never overwrite.
- It stays stable across pagination / filter / rerank, because cache hits do not rewrite metadata.
- It is what the search service returns to its callers as `requestId`, what is stamped into outbound third-party redirect URLs (for affiliate attribution), and what is forwarded to internal downstream services as their `correlationId` input.
- The name `request_id` is the consumer-facing label for what is stored internally as the metadata's `correlationId` field. Same value, two names.

### About search_id
- It is a **deterministic hash** of the search parameters (e.g. MD5) — content-addressed by definition.
- It is the **cache key**: looking up the cache by `search_id` returns all fields of the metadata record, including the stored `correlationId` (which is `request_id`). So `search_id` and `request_id` live in **the same cache entry**.
- It is the **only ID computable from the request itself** at lookup time — which is why it must be the cache key. You cannot look up by request_id, because for a fresh request you don't yet know which request_id corresponds to it.
- `search_id` may also be a first-class concept in **internal same-team** downstream services (writing it to MDC, using it as their own cache key). But it does **not** cross to external/third-party boundaries — those receive `correlationId` instead, since they don't share the producing team's domain vocabulary.

### About all three together
- **Lifecycle is identical** (one cache entry — they live and die together). What differs is:
  - `correlation_id`: scope = one gRPC hop; derivation = caller-supplied
  - `search_id`: scope = same-team service group; derivation = `hash(params)` (deterministic)
  - `request_id`: scope = all services downstream; derivation = first-writer-wins snapshot
- They cannot be merged because they answer **different questions**: cache lookup, batch attribution, cross-service tracing.

## Common misconceptions (flag immediately when learner says these)

| Misconception | Correct version |
|---|---|
| "Within a search session, correlation_id stays consistent under BFF" | Only **within a single inbound HTTP request**. Pagination / filter / rerank each open a new inbound and may bring a new correlation_id. |
| "request_id and search_id have different lifecycles" | **Same lifecycle** — they share the same cache entry. They differ in **derivation method and semantic scope**, not lifetime. |
| "We could just use search_id everywhere instead of request_id" | No. External / cross-team systems (third-party partners, bidding services) only understand the gRPC-standard `correlationId`. `search_id` is a producer-domain term that doesn't cross team boundaries (Conway's law). |
| "We could just use request_id as the cache key instead of search_id" | No. Cache lookup must use a key derivable from the **request alone**. request_id is only known **after** lookup hits, so it can't serve as the lookup key (content-addressed cache constraint). |
| "Front-end polling always corresponds to a back-end Poll RPC" | Not necessarily. Some services have the front-end repeatedly call a Create-style RPC instead, with cache-hit logic on the back-end making subsequent calls cheap. The "polling" can happen at the HTTP/gateway layer rather than at the gRPC service layer. |
| "request_id is just for log correlation" | It is also consumed for: third-party redirect URL attribution, internal ranking/bidding service input, shadow-mode comparison gating, and various response-proto fields exposed to callers. |
| "All three IDs are generated by the search service" | Only request_id (snapshot) and search_id (hash). correlation_id originates with the caller (front-end / gateway / test tool). |

## Per-round coverage checklist

For Rounds 2-5, the learner should touch the items below. Use this to judge whether a topic is `finished` or `unfinished`.

### Round 2 — Core Explanation
Required:
- Can name all three IDs and clearly distinguish them.
- States **why one ID is not enough** — caller-controlled values are not stable, but business logic (attribution, redirect, cache) needs stable identifiers.
- States the **ownership / control attribution** insight: an ID a service cannot control cannot carry that service's invariants.

### Round 3 — Implementation
Required:
- write-once mechanism: the metadata-initialization function runs only when no cache entry exists yet.
- Storage: a single cache entry with `search_id` as the key, all metadata fields (including `correlationId`) as fields within that entry.
- Propagation contrast: framework-provided channel-level interceptor (automatic, MDC → outbound gRPC) vs manual per-call-site passing (typical when no interceptor exists, prone to drift across endpoints).
- Bonus: mention the inbound server-side interceptor that extracts the correlation header into Context/MDC, and the named gRPC Context key used for the correlation ID.

### Round 4 — Trade-offs
Required:
- **Content-addressed cache constraint**: only a key derivable from the request (`search_id`) can serve as the lookup key. This is why `search_id` and `request_id` cannot be merged despite identical lifecycles.
- "Lifecycle identical ≠ identity semantics identical."
- **Conway's law**: ID propagation radius ≈ team collaboration radius. Same-team-internal services can share producer-domain IDs (e.g. `search_id`); cross-team boundaries (third-party / external services) fall back to gRPC-standard `correlationId`.
- Cost of multiple IDs: extra fields in metadata, mental overhead, debugging cost when they diverge.

### Round 5 — When to use / not use (or comparison summary for the group-summary topic)
Required:
- When you need to introduce a new ID layer: when the existing ID is controlled by a party who cannot guarantee the invariant you need.
- When NOT to: if a single existing ID already gives you both stability and content-derivability for your use case.
- For the **summary topic**, the learner should also produce a decision matrix: deterministic vs first-writer-wins vs caller-supplied — picked based on (a) what answers each can give and (b) who controls the value.

## Acceptance signals for the summary topic

A learner explaining the comparison well should be able to articulate at least:
1. The **four-step causal chain**: caller-controlled → unstable → need a stable export → request_id; but cache key needs to be derivable from request → search_id; lifecycles align (same cache entry) but semantic scopes differ.
2. Why none of the three can be dropped without losing a capability.
3. The cross-team boundary point: where the producer-domain ID (`search_id`) stops and the gRPC-standard `correlationId` takes over (the boundary between same-team internal services and external/third-party services).
