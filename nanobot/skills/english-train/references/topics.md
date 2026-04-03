# Backend Topic Pool

## Selection Rules

1. Pick **one specific topic** per session — never mix multiple topics in a single session.
2. Balance classic Backend topics with AI-era Backend topics over time.
3. Topics must be **small in scope but deep** — e.g., "why caching matters" not "system design overview."
4. If a topic from the previous day is marked `unfinished`, **continue it** before starting anything new.
5. Novelty must not override learnability — if a new topic is too hard for the learner's current level, downgrade to a more basic but still relevant entry point.
6. Prefer topics that let the learner reuse vocabulary or expressions from MEMORY.md's Knowledge Points Queue.
7. **Comparison topics** (those with "vs" or "trade-offs" comparing multiple items) — when selected from this pool, split them the same way as user-submitted comparison topics: train each item independently first, then run a comparison summary session last. Add them to Preferred Topics with a shared group tag.
8. **Topic relatedness**: when picking the next topic (from this pool or from Preferred Topics), prefer one that connects to the last finished topic. Relatedness includes:
   - Same technical domain (e.g., caching → database indexes → read-write separation)
   - Same problem class (e.g., rate limiter → circuit breaker → graceful degradation)
   - Progressive depth (e.g., connection pooling → distributed locking)
   - Traditional ↔ AI-era bridge (e.g., async processing → async task queues for AI workloads)
   This is a soft preference — if the learner's Knowledge Points Queue or level strongly suggests a different topic, that takes priority.

## Traditional Backend Topics

- Why caching matters and how to design a caching strategy
- What database indexes solve and when they hurt
- Why pagination is necessary in API design
- How to design a rate limiter
- How to diagnose API latency issues
- Why async processing improves throughput
- Message queue trade-offs (reliability vs. latency vs. complexity)
- How to explain a refactoring decision in Code Review
- Database read-write separation: when and why
- API design trade-offs (REST vs. gRPC, versioning, error contracts)
- Circuit breaker pattern and graceful degradation
- Connection pooling and resource management
- Distributed locking: use cases and pitfalls
- Log aggregation and structured logging strategies
- Database migration strategies in production
- Idempotency in API and job design
- Service discovery and load balancing basics
- Configuration management in distributed systems

## AI-Era Backend Topics

- How to design a backend API for an LLM-powered feature
- RAG system backend pipeline: retrieval, augmentation, generation
- Why AI requests need caching and rate limiting even more
- Handling high-latency AI inference in backend systems
- Designing async task queues for AI workloads
- Managing prompt, context window, and session state on the backend
- Tool calling orchestration from the backend perspective
- Why AI applications demand stronger observability
- Cost and throughput control for AI services
- Designing fallback mechanisms for AI features
- Vector search service integration and backend support
- Streaming response handling for LLM outputs
- AI model versioning and A/B testing infrastructure
- Guardrails and content filtering in AI backend pipelines
- Multi-model routing and gateway design
