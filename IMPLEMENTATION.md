# Implementation handoff

## Requested outcome

Build an original browser-based office in which a person can manage real projects and AI workers, inspect what each worker is doing and continue across sessions. Anyone should be able to self-host and add their preferred model provider or agent runtime.

This initial repository is intentionally specification-only. The initiating user asked for the GitHub project and sufficient guidance for another AI to implement it, rather than an application in the preparation session.

## Start with M0, then deliver M1 end to end

1. Read the shared state and the requirements. Preserve the first-release scope rather than building a full autonomous company.
2. At M0, create a TypeScript monorepo with the package boundaries in `docs/architecture.md`. Use Node.js 24 LTS initially, check supported maintained patch versions, select one pnpm version and commit the resulting lockfile. Set up typechecking, linting and unit/E2E tools. Do not require any API credential to bootstrap.
3. Implement the event reducer and persistence, not animation-driven statuses.
4. For M1, implement a clearly labelled demo with one project/room, two workers and a deterministic task stream. Display its task/evidence panel in the browser and its equivalent accessible list.
5. Reload, reconnect and deduplicate events. Demonstrate a stale worker and a rejected approval without pretending anything was executed.
6. Capture the real browser at desktop/mobile sizes. Link each piece of evidence to requirement IDs. Continue with M2 only after M1 criteria pass.

## First visible demonstration

The owner opens the app without credentials, selects “Try demo” and sees an original isometric office. A worker starts a synthetic task. Clicking the worker reveals a timeline and a synthetic artifact. The second worker waits for approval. Approving resumes only the mock runtime, with the demo marker still visible. Refreshing preserves the same task identities and does not create a second attempt. Switching to list view exposes the same statuses and actions by keyboard.

## Release sequence

| Milestone | Deliverable | Gate |
|---|---|---|
| M0 | Runnable skeleton and contract validation | Fresh checkout setup documented and checks pass |
| M1 | Deterministic office, panels, persistence, accessible list | No key/model required; replay/reconnect and evidence agree |
| M2 | Projects/tasks and capability-driven adapters | Conformance tests with mock and two distinct protocols |
| M3 | Opt-in real execution on an isolated workspace | Policy enforcement, approvals, cancellation and cost caps tested |
| M4 | Markdown memory and optional Obsidian | Scoped read/write, conflicts, provenance and prompt-injection cases tested |
| M5 | Distribution and hardening | Self-host instructions and honest support matrix |

Detailed work packages and acceptance gates are in [the backlog](docs/backlog.md).

## Definition of done for a work package

Runnable behavior, appropriate automated tests, verified browser behavior where applicable, updated docs/state, and no misleading success/compatibility claim. Report unavailable credentials or external acceptance as limitations rather than using a mock and calling the integration complete.

## Defaults resolved here

- Single-host, single-owner local edition first; no commercial SaaS, organization billing or multi-tenant login required in M1.
- Loopback binding by default; remote access is a later authenticated deployment mode.
- English UI first with translation keys; Spanish is the next locale. Never bake translation strings into sprites.
- Original 2D isometric art; no user-provided copyrighted screenshot is distributed.
- MIT license; no analytics or third-party network calls until an integration is explicitly enabled.
- Optional integrations may have provider-specific cost and authorization requirements. No promise that an existing ChatGPT/Copilot subscription can be used through an unrelated API.

## Initial task prompt

> Implement M0 and M1 of Agent Office. Read AGENTS.md and the referenced acceptance criteria. Build a runnable local demo, with the isometric scene and an accessible list backed by the same persisted event stream. Do not contact model providers, execute host shell tools, import personal knowledge or mark M2+ complete. Keep the current state document accurate and include browser evidence and reproducible commands when finished.
