# 0001: Modular Event-Driven Pipeline

## Status

Accepted

## Context

Spacei is a local learning project for streaming open space data. The project should make Kafka/Event Hubs concepts visible while staying small enough to write and understand by hand.

The application also needs to support read-side use cases such as querying the latest satellite state and later visualising positions on a 3D globe.

## Decision

Use a modular event-driven pipeline with CQRS-style projections:

```text
external sources
  -> ingestors
  -> Redpanda raw topics
  -> normalizers
  -> Redpanda normalized topics
  -> projectors
  -> SQLite read models
  -> API/export
  -> 3D globe
```

Redpanda is the durable event stream. SQLite is a local read model used for queryable state, idempotency, replay checks, and future visualisation exports.

The codebase starts as one Python application with separately runnable modules rather than separate services.

## Consequences

- We learn real streaming concepts: topics, partitions, offsets, consumer groups, replay, lag, and dead-letter handling.
- Each module has one clear responsibility.
- SQLite state can be deleted and rebuilt from Redpanda events.
- The system has more moving parts than a single Python script, but that complexity is intentional for learning.

