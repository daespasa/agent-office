# ADR 0001: local web foundation and original 2D office

Status: accepted as initial implementation direction, 2026-10-30. No dependencies installed yet.

## Context

The product needs a browser UI, a lively office and reliable operational detail without binding anyone to one model service. The first delivery should be runnable locally with no credentials.

## Decision

TypeScript shared wire contracts; React/Vite for accessible panels; PixiJS for the 2D scene; Fastify on supported Node.js LTS; SQLite/WAL for the initial single-host event/job store; SSE for server-to-browser events and HTTP commands. Start with Node 24 LTS for its established ecosystem, validating maintained patch versions at M0. Pin actual dependency versions and package manager in the implementation lockfile.

Keep a first-class DOM/list representation. Use original isometric office assets. Start with a deterministic mock and bounded project count. No separate 3D engine, mandatory cloud backend, Redis or SaaS account for M1.

## Alternatives and consequences

A DOM-only scene simplifies tooling but becomes awkward for depth/sprites/camera; keep DOM for accessible controls regardless. A full game engine adds systems the task manager does not need. A serverless-only backend complicates durable local execution. SQLite is not a promise of distributed multi-writer scale; moving to multi-host needs a later storage/lease ADR.

Sources: [Node release policy](https://nodejs.org/en/about/previous-releases), [PixiJS guides](https://pixijs.com/8.x/guides/). These sources inform stack choice, not a claim that the future dependency graph is tested.
