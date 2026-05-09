# 0004: Source Ingestors

## Status

Accepted

## Context

Source APIs and files have their own formats, reliability characteristics, timestamps, and identifiers. The rest of the pipeline should not depend on source-specific fetch details.

## Decision

Each source has an ingestor module. The first planned source is CelesTrak TLE data.

An ingestor:

- fetches source data
- wraps source records in raw event envelopes
- publishes raw events to Redpanda
- does not write SQLite
- does not perform domain normalization beyond the minimum needed to create stable event IDs and keys

## Consequences

- Adding a new source means adding a new adapter and raw topic.
- Raw events preserve source-shaped data for replay and parser changes.
- Ingestors stay small and testable.

