# Test strategy and evidence

## Handoff checks available today

`python3 scripts/check_spec.py` checks local Markdown links, required documents, JSON syntax/local schema refs, example configuration and the deterministic event lifecycle. It is a small consistency check, not an application test suite or a full JSON Schema implementation.

## Implementation layers

- Domain: legal/illegal transitions, terminal immutability, attempt retry identities, task verification independent of execution, budget unknowns and approval scopes with an injected clock.
- Persistence: transactional outbox/leases, fenced writes, replay ordering, idempotency keys and migration recovery against a temporary database.
- Adapters: shared conformance suite plus protocol fixtures; real provider tests opt-in, bounded and explicitly credentialed. Mark results mock vs live and never require live credentials in default CI.
- UI: Playwright journeys on the real app, important controls by accessible role, actual network/event assertions and step-specific screenshots. Capture filter/approval/recovery states before clearing them, not only the restored screen.
- Accessibility: keyboard and list parity, focus management, live-region throttling, contrast, reduced motion and mobile workflows.
- Security: policy denial, path/symlink traversal, XSS, SSRF, prompt injection and stale approvals.

## Mandatory journeys

| Test | Journey | Requirements |
|---|---|---|
| T01 | Fresh demo → room/worker → timeline and synthetic artifact | AO-01,05,07,12 |
| T02 | Same actions using keyboard/list at 360 px | AO-02,07 |
| T03 | Refresh/reconnect → no duplicate task or attempt; missing cursor reconciles | AO-06,14 |
| T04 | Approve/reject/expire exact mock action; replay decision denied | AO-08,14 |
| T05 | Runtime disconnect → stale worker, preserved attempt; no fake failure/success | AO-05,14 |
| T06 | Mock + two provider protocols through same conformance tests | AO-03,15 |
| T07 | Create/select project; cross-project read/tool action denied | AO-13,16 |
| T08 | Budget exhausted/usage unknown; no accidental zero-cost claim | AO-10 |
| T09 | Cancel completion race/retry; external effects not replayed automatically | AO-06,08,14 |
| T10 | Save curated Markdown; manual edit conflicts preserved | AO-11 |
| T11 | Malicious note/artifact tries privilege escalation | AO-08,11,13 |

Use synthetic projects, local fixtures and disposable workspaces. Destructive tests must create their own prefixed records and clean up only those records. A green resource-loading check is not evidence that task workflows work. Add screenshots and assertions at the state being tested, plus JSON test results; do not use screenshots alone as proof.

## CI growth

Today: handoff checker only. M0: typecheck/lint/contracts/unit/build. M1: isolated deterministic browser E2E and screenshots. M2+: conformance tests and scheduled opt-in checks if explicitly configured; no default paid background job. Publish named test results and diagnostic artifacts with secret-safe retention. Do not claim the whole product passes because documentation checks pass.
