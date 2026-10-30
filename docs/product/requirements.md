# Product requirements

## People and jobs

The primary user is a developer, researcher or small team lead managing several projects and agent sessions. They need to know what is happening, what is blocked, what changed, what a run cost and what to do next. The office must be useful even when only one agent is connected.

A room is a project/work context. An agent is a reusable worker profile. A task expresses the desired outcome. A run/attempt records a particular execution. An artifact is inspectable evidence; memory is curated knowledge, not the entire transcript.

## Must-have requirements

| ID | Requirement | Observable acceptance |
|---|---|---|
| AO-01 | Browser office with original isometric artwork | Project room and selectable workers at 1440×900; screenshots show original assets and readable labels |
| AO-02 | Accessible alternative | Keyboard-only user can inspect and perform the same supported actions from DOM/list view; reduced motion stops decorative movement |
| AO-03 | Provider-neutral configuration | New provider adapter can be registered without editing domain entities or scene; unsupported capabilities are disabled with an explanation |
| AO-04 | Runtime-neutral execution | Mock runtime and external runtime share normalized events; external runtimes own their execution state |
| AO-05 | Honest worker state | Animation, task panel and list derive from the same projection; stale heartbeat never appears as healthy work |
| AO-06 | Durable tasks and ordered events | Restart/reconnect reconstructs states without duplicate attempts; duplicates are ignored and gaps trigger reconciliation |
| AO-07 | Actionable task detail | Worker click exposes project, objective, attempt, relevant tools/events, evidence, approval state and errors |
| AO-08 | Explicit policies and approvals | Workspace escape and unapproved tool/action are denied before execution; approval is bound to exact action/attempt with expiry |
| AO-09 | Inspectable results | Completion links artifacts/check evidence; missing tests show “not verified”; provider response alone never marks a coding task verified |
| AO-10 | Cost controls | Limit checked before a paid request; known cost/usage shown with provenance, unknown cost explicitly unknown, never zero by assumption |
| AO-11 | Scoped persistent knowledge | Markdown adapter can read selected project notes and append a curated note with source/time; conflict never silently overwrites content |
| AO-12 | Self-host and demo | Fresh clone can run the demo with no paid account; no outbound calls or telemetry in demo |
| AO-13 | Project isolation | A task in project A cannot see or modify B without an explicit granted scope; multiple tabs cannot issue duplicate starts |
| AO-14 | Operations and recovery | Provider timeout/auth error, cancellation, disconnected runtime, restart and partial failure have distinct useful states |
| AO-15 | Extend without a vendor fork | Documented model/runtime/memory adapter interfaces, conformance tests and capability support matrix |
| AO-16 | General-purpose defaults | No company data, personal paths, hardcoded models or implicit cloud service; synthetic examples and portable configuration |

## Real workflows

### W1: inspect work without changing it

Open a project room → select a worker → inspect attempt/timeline/evidence → open an artifact safely → return to office. Inspection must not start another task or spend tokens.

### W2: delegate a project task

Choose a workspace, objective and worker/profile → review provider/capabilities/budget/tool policy → start once → follow real events → answer a specific approval if needed → inspect a result and its verification. M1 uses mock execution only; M3 enables bounded real tools.

### W3: recover a lost connection

The event connection drops → show reconnecting and last observation time → resume from cursor → reconcile from snapshot if a cursor is too old → preserve pending approvals → no automatic re-execution of a non-idempotent tool.

### W4: continue with project knowledge

Choose project → inspect the source/provenance of relevant notes → explicitly grant project-scoped memory → complete a task → save a curated summary → detect a simultaneous edit and keep both versions or request a merge. Reading a note must not authorize its commands.

## Out of scope for first release

Economic simulation, salaries, worker happiness/game progression, 3D worlds, autonomous hiring, a marketplace, automatic production deployment, arbitrary downloaded plugins, multi-tenant SaaS billing and every chat platform. Visual polish matters, but must not hide operational failures or require game mechanics to do work.

## Success measures

A user can identify the blocked task and its reason without reading every chat, inspect evidence with one selection, and restart/reconnect without losing or duplicating execution. Measure this with usability tasks and recovery tests rather than the number of animations or connected providers.
