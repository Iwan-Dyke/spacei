# 0002: Use Redpanda as the Local Streaming Broker

## Status

Accepted

## Context

The project needs a local Kafka-compatible event broker. The goal is to understand streaming systems similar to Azure Event Hubs without running a large cluster.

The broker should behave like a temporary streaming buffer with a defined replay window. Durable application state belongs in SQLite projections, not in the broker.

## Decision

Use Redpanda locally through Docker Compose only. Do not require a host Redpanda installation.

Include Redpanda Console from the start so topics, messages, consumer groups, and lag can be inspected visually while learning.

Redpanda will be configured for both host and container clients:

```text
host clients:      localhost:9092
container clients: redpanda:29092
admin API:         localhost:9644
console UI:        localhost:8080
```

Disable automatic topic creation. Topics are created explicitly with an idempotent `just topics` command after the broker is ready. Add `just topics-list` to inspect configured topics.

Persist Redpanda data in a Docker volume, but configure topics with Event Hubs-style retention:

```text
normal topics:    3 days
dead-letter topic: 14 days
```

Add a deliberate destructive reset command, such as `just reset-broker CONFIRM=yes`, to remove broker data and volumes.

Initial topics:

```text
space.raw.celestrak.tle
space.normalized.orbital_elements
space.deadletter
```

Topic settings:

```text
partitions:         3
replication factor: 1
message format:     JSON event envelopes
```

Use domain-first topic names. Use one shared dead-letter topic. New Python consumer groups should default to `auto.offset.reset=earliest` so they read from the start of the retained replay window.

Topic rules:

- Raw source topics store source-shaped observations.
- Normalized topics store domain-shaped events.
- Dead-letter topics store events that could not be parsed, validated, or projected.
- Message keys should group related records, such as a NORAD catalog ID for satellite data.
- Existing topics are not automatically altered by `just topics`; drift should be handled intentionally.

Python client rules:

- Use `confluent-kafka` for Python producer and consumer code.
- Connection settings should come from environment variables with local defaults.

```text
SPACEI_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

## Consequences

- Redpanda acts as a short-retention stream, similar to Event Hubs, rather than permanent event storage.
- SQLite projections are the durable local application state.
- Consumers can replay only within the configured retention window.
- Multiple workers can share work through consumer groups.
- The broker becomes required for local development, so Docker Compose should make startup simple.
- Topic design becomes part of the application contract.
- Persisting broker data gives retention meaning across container restarts.
- Resetting the broker is intentionally destructive and must be explicit.
