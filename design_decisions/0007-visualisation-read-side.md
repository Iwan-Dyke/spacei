# 0007: Visualisation Read Side

## Status

Accepted

## Context

The project may later show satellite data on a 3D globe. A globe needs render-friendly position data, not raw TLE events.

## Decision

Treat visualisation as a read-side concern. The globe reads from an API or static export built from SQLite read models.

The pipeline should later add a position sampler/exporter:

```text
SQLite latest orbits
  -> orbit propagation
  -> sampled positions
  -> API/static JSON
  -> 3D globe
```

Use a real SGP4 implementation for orbit propagation when that stage begins.

## Consequences

- The frontend does not need to consume Redpanda directly.
- Orbital math stays in a testable backend module.
- The rendering model can be optimized for the globe without changing ingestion or normalization.

