# 0006: SQLite Projectors

## Status

Accepted

## Context

Redpanda is good for durable event history, but UI and analysis features need queryable local state. SQLite is enough for local development and keeps operations simple.

## Decision

Projectors consume normalized events and write SQLite read models.

Initial tables:

```text
processed_events(event_id primary key, topic, processed_at)
space_objects(norad_id primary key, name, updated_at)
orbital_element_sets(event_id primary key, norad_id, epoch, line1, line2, source)
latest_orbits(norad_id primary key, event_id, epoch, updated_at)
```

Projectors must be idempotent. Replaying a topic from offset `0` should not duplicate data.

## Consequences

- SQLite can be deleted and rebuilt from Redpanda.
- `processed_events` lets consumers safely handle repeated deliveries or replays.
- Read models can be shaped for use cases instead of mirroring event payloads exactly.

