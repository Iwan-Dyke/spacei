# 0005: Normalizers

## Status

Accepted

## Context

Raw source records are not ideal for domain logic, querying, or visualisation. The project needs a boundary where source-shaped data becomes domain-shaped data.

## Decision

Normalizers consume raw topics and publish normalized domain events.

For TLE data, the normalizer consumes:

```text
space.raw.celestrak.tle
```

and publishes:

```text
space.normalized.orbital_elements
```

A normalizer:

- validates raw event envelopes
- parses source payloads
- emits domain-shaped events
- publishes invalid records to `space.deadletter`
- does not write SQLite

## Consequences

- Parser bugs are isolated from ingestion.
- Normalization can be replayed if the parser improves.
- The normalized topic becomes the contract for downstream projectors and visualisation.

