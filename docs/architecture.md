# Architecture

## Foundation

Single-host local edition, with an accessible browser UI and a server-side execution boundary. Proposed monorepo:

```text
apps/web/                  React/Vite DOM panels and accessible list
apps/server/               Fastify HTTP/SSE entry points
apps/worker/               Durable task consumer and isolated execution host
packages/domain/           Entities, state transitions, policies; no IO
packages/application/      Use cases and ports
packages/contracts/        Runtime event/config validators and shared wire types
packages/scene/            PixiJS office; consumes read-only projection
packages/adapters/         Model/runtime/memory/storage implementations
packages/testing/          Mock runtimes, clocks, replay and conformance fixtures
```

These directories describe the target; they are not created as empty packages in this handoff. At M0 create only packages used by the vertical slice. Do not add a monorepo manager just to host folders.

Dependency direction: UI/transport/adapters → application → domain. Shared wire contracts may be consumed by UI and server; persistence entities are private. Rendering never imports credentials, SDKs, execution services or database clients.

## Domain

| Entity | Important fields and responsibilities |
|---|---|
| Workspace | Owner scope and accessible project roots |
| Project | Stable ID, display name, room/layout, granted root and memory scope |
| AgentProfile | Role label, runtime/model refs, capability intersection, tool/spend policy |
| Task | Project, objective, assignment, desired outcome, status, verification |
| Attempt | Task ref, runtime session, state, lease/fence, timestamps, usage |
| Approval | Exact action hash, attempt/lease, requester, expiry and decision |
| Event | Versioned envelope, source, stream cursor, occurrence/observation times |
| Artifact | Typed reference, provenance, digest, availability and safe preview policy |
| KnowledgeNote | Scope, path/ref, revision/hash, provenance and reviewed timestamp |

Task states: `draft`, `queued`, `in_progress`, `needs_review`, `completed`, `failed`, `cancelled`. Verification is separate: `not_run`, `passed`, `failed`, `unknown`. A successful attempt can place a task in `needs_review`; explicit acceptance or configured deterministic checks decide completion. Repeating work creates a new attempt, never rewrites a terminal attempt.

Agent availability: `available`, `busy`, `offline`, `unknown`. Stale heartbeat affects observed availability, not the durable attempt's terminal status.

## Ports

- `ModelProvider`: inference/capability/usage normalization; no shell or workflow scheduling.
- `AgentRuntime`: start/observe/cancel sessions and normalize activity; pause/resume/approve only when supported. An external runtime's events are authoritative for its own run.
- `ToolExecutor`: bounded action execution governed by host policy; never an unrestricted process inherited from a model response.
- `MemoryStore`: scoped search/read/propose-write/commit with expected revision.
- `EventStore`, `TaskRepository`, `ApprovalRepository`, `ArtifactStore`, `Clock`, `SecretStore`.

## Execution and event flow

User command → authenticated API/policy checks → persisted command/task + outbox in one transaction → worker lease → runtime adapter → normalized append-only events → projector/read model → SSE cursor → accessible UI and office projection.

M1 uses a mock worker with no tools or network. Keep that demo path separate from real execution mode. SSE is server-to-browser; commands use idempotent HTTP requests.

SQLite WAL is sufficient for one host. Durable jobs/outbox and transactional leases live in SQLite, not process memory or Redis by default. A fencing token prevents an old worker from updating a newly acquired attempt. Claim/heartbeat/cancel/recovery operations need race tests. External effects are not exactly-once: after a crash reconcile unknown tool outcome instead of automatically retrying a dangerous action.

Persist canonical event sequence per workspace; normalize producer events into that order. An envelope's event ID and source idempotency key prevent duplicates. The HTTP/SSE contract, replay and retry rules are in [the event protocol](../contracts/events.md).

## Security and deployment boundaries

The server holds provider credentials; the browser only sees connection metadata and secret references. Bind to loopback by default and validate Origin/Host. Remote access requires authentication, authorization, TLS and CSRF-safe command transport; no public unauthenticated remote mode. See [security model](security-model.md).

A project root is a scope boundary, not a sufficient sandbox. M3 tool execution requires an isolated container/worker with bounded mounts/resources/network and no host Docker socket. A process working directory alone is not isolation. Unsupported sandbox platforms stay observation/mock-only.

## Persistence and migration

Version migrations from M0; forward migrations plus documented backup/restore for the single-host store. Keep event schema version separate from DB schema version. Store event metadata and artifact references, not unbounded raw provider payloads. Define retention and deletion/export policy. Credentials never go in events, Markdown exports, fixtures or browser localStorage.

## Decisions and open issues

Initial stack and tradeoffs: [ADR 0001](adr/0001-foundation.md). Provider/runtime split: [ADR 0002](adr/0002-adapters.md). Event truth and knowledge: [ADR 0003](adr/0003-state-and-memory.md).

Later decisions: multi-user authentication provider, hosted tenant isolation, distributed queue, final art pipeline and optional third-party runtime versions. Do not build these as hidden requirements of the local demo.
