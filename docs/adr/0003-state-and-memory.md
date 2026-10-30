# ADR 0003: observed events drive the office; curated knowledge preserves continuity

Status: accepted, 2026-10-30.

## Context

A visual worker can easily create a false impression of activity or success. A memory log can also make an old observation look like a current authorization.

## Decision

Use durable ordered events and a replayable read projection as the single source for the scene, list and detail panel. Separate agent availability, attempt lifecycle, task status and verification. Keep explicit demo/live namespaces and stale observations.

Memory contains curated, scoped Markdown with sources/revisions; hooks may record activity metadata but do not constitute verified decisions. Notes cannot grant tools or permission. Repository technical decisions stay in versioned source docs; copies carry provenance and historic/stale markers.

## Consequences

More state modelling and recovery tests are required. Animation/pathfinding has no execution authority. Missing evidence is visible. Reconnecting cannot turn an unknown operation into a guaranteed retry. Knowledge writes require revision conflict handling.
