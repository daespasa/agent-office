# Event and command protocol v1

This is a normative target contract, not an existing server. [event.schema.json](event.schema.json) defines the envelope shape. [demo-events.ndjson](../examples/demo-events.ndjson) is a deterministic synthetic stream.

## Envelope and ordering

Every event contains `schemaVersion`, `eventId`, `workspaceId`, `projectId`, `sequence`, `occurredAt`, `observedAt`, `source`, `mode`, `type`, `data`. `agentId`, `taskId`, `attemptId`, `correlationId` are included when the event belongs to those entities. Times are UTC RFC3339. Sequence is assigned transactionally by EventStore within the workspace; it is not trusted from an external producer. Persist the producer event/session identity to deduplicate ingress.

`mode` is `demo` or `live`. Do not mix modes in the same workspace stream or task. Demo markers appear in every result/evidence view and exports. Unknown event types or schema versions produce a visible compatibility/reconciliation error, never an implied completion.

## Attempt lifecycle

Allowed transitions:

```text
queued -> running | cancelled | failed
running -> waiting_approval | succeeded | failed | cancel_requested
waiting_approval -> running | failed | cancel_requested
cancel_requested -> cancelled | succeeded | failed
```

Terminal states never return to running. A retry creates a new attempt. `succeeded` after `cancel_requested` is allowed if the remote runtime completed before cancellation took effect; show that race honestly. A queued attempt can fail startup. `approval.rejected` fails the waiting attempt with reason `approval_rejected` in v1. Expiry requires a fresh action request; no automatic execution. A disconnect is an observation event, not a lifecycle transition.

## Event payloads

| Type | Required data | Semantics |
|---|---|---|
| `agent.availability.changed` | `availability` | `available`, `busy`, `offline`, `unknown`; last-seen is explicit |
| `attempt.state.changed` | `state`; `reason` for failure | Legal transition; requires task/attempt/agent IDs |
| `attempt.progress` | `message` | Safe public progress only; not chain-of-thought |
| `approval.requested` | `approvalId`, `actionHash`, `expiresAt`, `summary` | Bound to exact attempt/action |
| `approval.resolved` | `approvalId`, `decision` | `approved`, `rejected`, `expired`; apply once |
| `artifact.created` | `artifactId`, `kind`, `label`, `ref`, `sha256` | Evidence reference, never an unchecked host path |
| `usage.reported` | `inputTokens`, `outputTokens`, `cost`, `currency`, `basis` | Nullable unknowns; reported/estimated basis |
| `runtime.connection.changed` | `status` | `connected`, `reconnecting`, `disconnected`; do not mutate attempt status |
| `task.verification.changed` | `status`, `evidenceRefs` | `not_run`, `passed`, `failed`, `unknown`; passed/failed requires evidence |

The initial JSON Schema constrains envelope/type fields and critical lifecycle/approval data. Implement type-specific runtime schemas for every payload in M0 before accepting network events; this handoff does not claim exhaustive payload validation.

## HTTP/SSE target

- `GET /api/v1/workspaces/:id/snapshot`: snapshot + last cursor, authorized scope, contract version.
- `GET /api/v1/workspaces/:id/events`: SSE `id` is workspace sequence; resume via Last-Event-ID. Retention gap yields a reconciliation response/event that forces a fresh snapshot. Snapshot and live subscription must have no race gap.
- `POST /api/v1/projects`, `/tasks`, `/tasks/:id/start`, `/attempts/:id/cancel`, `/approvals/:id/resolve`: owner scope plus validated payload and `Idempotency-Key` for mutations. These are relative to `/api/v1`; store request fingerprint and replay response; reusing key with changed payload returns 409.
- Artifacts served through authorized IDs, not arbitrary filesystem-path parameters.
- Configuration endpoints return secret refs/connection status only. A separate secret write flow never echoes the value.

SSE heartbeats carry no semantic task status. A client deduplicates by eventId/sequence, checks gaps and reconciles. An external event producer authenticates to a server-controlled ingest adapter; browsers never append authoritative lifecycle events directly.

Errors: stable machine code, safe message, retryability and request ID. 400 malformed; 401/403 auth/scope; 409 state/idempotency conflict; 422 unsupported capability; 429 policy/rate cap; 503 transient runtime/provider. Retry only explicitly retryable and idempotent operations with bounded backoff and Retry-After.
