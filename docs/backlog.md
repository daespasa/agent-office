# Ordered implementation backlog

All boxes start unchecked. A checkbox changes only with runnable behavior and linked evidence. Requirements are in [the product spec](product/requirements.md).

## M0 — Foundation

- [ ] B001 Create only the used monorepo packages, actual package manifests, compatible versions and committed pnpm lockfile; document fresh-clone commands. AO-12,16.
- [ ] B002 Implement strict per-type contract validators and replay reducer from the fixtures, rejecting malformed/unknown payloads. AO-05,06.
- [ ] B003 SQLite migrations/event store/outbox with workspace sequence and idempotency. Validate terminal transitions and separate verification. AO-06,09.
- [ ] B004 Typecheck, lint, unit, contract and build CI with no secrets/network model calls. AO-12.

Gate: fresh checkout builds and strict fixture validation passes; invalid lifecycle/payload cases fail.

## M1 — Office demo vertical slice

- [ ] B010 Accessible DOM shell and list, original isometric scene, semantic tokens and selection drawer. AO-01,02,07.
- [ ] B011 Mock runtime/clock with labelled persistent demo namespace and known artifact. AO-05,09,12.
- [ ] B012 Snapshot/SSE recovery, deduplication and stale heartbeat view. AO-06,14.
- [ ] B013 Exact mock approval approve/reject/expire; cancellation acknowledgement and race. AO-08,14.
- [ ] B014 End-to-end journeys T01–T05; desktop/mobile/reduced-motion evidence from the actual app. AO-01,02,05–09,12,14.

Gate: first demonstration in IMPLEMENTATION.md works without credentials. No shell/model work occurs. Original concept/fixtures are not used as fake screenshots of the app.

## M2 — Projects and extensible connections

- [ ] B020 Project/task/profile CRUD with persistent IDs, safe root selection and runtime/model separation. AO-03,04,13,16.
- [ ] B021 Connection setup/secret store/capability matrix; no secrets returned to browser. AO-03,08.
- [ ] B022 Configurable compatible-HTTP and Anthropic-native adapters plus common conformance tests; official protocol/auth notes. AO-03,15.
- [ ] B023 Budgets/reservations/known-vs-unknown usage and sanitized timeout/rate/auth errors. AO-10,14.
- [ ] B024 External runtime adapter reference plus observe-only contract/reconcile tests. AO-04,15.

Gate: mock and two model protocol adapters pass conformance. A real acceptance claim requires a separate opt-in run and date; absence of credentials must be reported accurately.

## M3 — Bounded real work

- [ ] B030 Isolated execution host, leases/fencing, mounted workspace and network/resource/tool policies. AO-08,13.
- [ ] B031 Tool plan/proposal + argument-bound approvals; no model-sourced policy escalation. AO-08.
- [ ] B032 Artifact collection with hashes/provenance and separate check verification. AO-07,09.
- [ ] B033 Cancellation/restart/unknown effect recovery and duplicate browser start race. AO-06,14.
- [ ] B034 A disposable real task writes a small project file, runs its bounded check and exposes evidence. AO-07–09.

Gate: all security/recovery tests pass before enabling host-affecting tools. Never use production projects for the first acceptance test.

## M4 — Knowledge

- [ ] B040 Scoped Markdown memory adapter, source refs and curated closeout summaries. AO-11.
- [ ] B041 Revision conflicts/manual edits, historical source status and injection tests. AO-08,11.
- [ ] B042 Optional Obsidian configuration and portable import/export, with no plugin dependency. AO-11,16.

Gate: edited note is preserved; another project/secret path cannot be read; notes never expand authorization.

## M5 — Distribution and polish

- [ ] B050 Original sprite/tile kit with provenance/license inventory and responsive office polish. AO-01,02.
- [ ] B051 Container/self-host install, backup/restore, support matrix, retention and deletion. AO-12,14,16.
- [ ] B052 Authenticated remote mode only with all workspace/event/artifact authorization controls. AO-08,13.
- [ ] B053 Translation keys and Spanish locale; community adapter guide/example; release checklist. AO-15,16.

Later: optional Hermes/CLI adapters after validating their official lifecycle/control/auth interfaces; scheduling, multi-user roles and more layouts. These are not prerequisites for M1 and not automatic compatibility claims.
