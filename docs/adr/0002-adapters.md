# ADR 0002: separate model providers, execution runtimes and memory

Status: accepted, 2026-10-30.

## Context

“Any AI provider” can mean a model HTTP API, a local inference server or a complete external coding agent. They expose different control, permission and billing semantics.

## Decision

Define separate ModelProvider, AgentRuntime, ToolExecutor and MemoryStore ports. Declare capabilities and normalize events/errors without leaking SDK types into the domain. Hermes is an optional runtime adapter, not the foundation. Plain Markdown is an optional memory adapter, not a required Obsidian installation.

## Consequences

Adapters need conformance tests and protocol/version documentation. Unsupported features remain unavailable. Compatible chat HTTP does not imply tool/cancellation/session compatibility. Existing consumer subscriptions are never assumed to provide API entitlement. See [adapter contract](../adapters.md).
