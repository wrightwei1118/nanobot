# Article Categories — 种子类别和命名规范

## Naming Conventions

- Use **English**, title-cased (e.g., "Prompt Engineering" not "prompt engineering")
- Keep names **short and specific** — 1-3 words preferred
- Avoid overly broad terms like "AI", "Backend", "Programming"
- When in doubt, prefer the term most commonly used in the technical community

## Seed Categories

### AI / LLM

| Category | Covers |
|----------|--------|
| RAG | Retrieval-augmented generation, chunking, retrieval strategies |
| RAG Pipeline | End-to-end RAG system design, indexing, orchestration |
| Prompt Engineering | Prompt design, few-shot, chain-of-thought, system prompts |
| Agent Framework | LangChain, CrewAI, AutoGen, agent architectures |
| Agent Skill | Individual agent capabilities, tool use patterns |
| Multi-Agent System | Agent collaboration, orchestration, communication |
| Function Calling | Tool use, function calling APIs, structured output |
| Fine-Tuning | Model fine-tuning, LoRA, RLHF, training data |
| LLM Inference | Serving, quantization, batching, latency optimization |
| LLM Evaluation | Benchmarks, eval frameworks, quality metrics |
| Vector Database | Pinecone, Weaviate, Milvus, pgvector, similarity search |
| Embedding | Embedding models, semantic similarity, representation |
| Knowledge Graph | Graph-based knowledge, entity relationships, GraphRAG |
| Multimodal AI | Vision-language models, image understanding, audio |
| AI Safety | Alignment, guardrails, content filtering, red teaming |
| MCP | Model Context Protocol, MCP servers, tool integration |

### Software Engineering

| Category | Covers |
|----------|--------|
| System Design | Architecture patterns, scalability, high-level design |
| Distributed Systems | Consensus, replication, partitioning, CAP theorem |
| Microservices | Service mesh, decomposition, inter-service communication |
| API Design | REST, gRPC, GraphQL, API versioning, contract design |
| Database | SQL, NoSQL, query optimization, data modeling |
| Caching | Redis, Memcached, caching strategies, invalidation |
| Message Queue | Kafka, RabbitMQ, event-driven architecture, pub/sub |
| DevOps | CI/CD, deployment strategies, infrastructure as code |
| Observability | Monitoring, logging, tracing, alerting |
| Testing Strategy | Test design, test pyramid, integration testing |
| Performance | Profiling, optimization, load testing, benchmarking |
| Security | Authentication, authorization, encryption, OWASP |
| Container | Docker, Kubernetes, orchestration, service mesh |

### Programming

| Category | Covers |
|----------|--------|
| Design Patterns | GoF patterns, architectural patterns, idioms |
| Concurrency | Threading, async, parallelism, synchronization |
| Data Structures | Trees, graphs, hash maps, specialized structures |
| Type Systems | Static typing, generics, type inference |
| Functional Programming | Immutability, monads, pure functions, composition |

## Adding New Categories

When creating a new category not listed here:

1. Check if an existing category already covers the topic — avoid duplication
2. Follow the naming conventions above
3. Keep it at the right granularity — specific enough to be useful, broad enough to collect multiple articles
4. Examples of good new categories: "Streaming Architecture", "Feature Store", "Synthetic Data", "Code Review"
