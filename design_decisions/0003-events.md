# 0003: Event Envelope

## Status

Accepted

## Context

Different sources and pipeline stages need a consistent event shape. The envelope should support tracing, idempotency, schema evolution, and dead-letter handling.

## Decision

All Redpanda messages use a JSON event envelope:

```json
{
  "event_id": "celestrak:tle:25544:2026-05-09T19:00:00Z",
  "event_type": "tle.observed",
  "source": "celestrak",
  "schema_version": 1,
  "observed_at": "2026-05-09T19:00:00Z",
  "ingested_at": "2026-05-09T19:01:12Z",
  "payload": {}
}
```

Use JSON first. Do not introduce Avro, Protobuf, or Schema Registry until the basic streaming flow is working.

## Consequences

- Events are easy to inspect by hand.
- `schema_version` leaves room for future format changes.
- `event_id` gives consumers a stable idempotency key.
- JSON is less strict than a schema registry, so tests must validate expected event shapes.

