# Contributing

The project is currently a specification and implementation handoff. Start with [IMPLEMENTATION.md](IMPLEMENTATION.md); do not assume an application already exists.

Keep changes scoped to a milestone and reference AO/B IDs. Record material architecture changes in ADRs, update shared state, and provide reproducible validation. Use Conventional Commits. Tests should validate behavior, recovery and security boundaries rather than duplicate implementation details.

Default checks must require neither a provider account nor paid/network model calls. Any real integration test must be explicitly enabled with disposable data, bounded spending and sanitized evidence. Do not publish local configuration, personal memory or production details.

Add new provider/runtime/memory integrations through the ports and conformance suite. No mandatory vendor, undocumented auth mechanism or copied game artwork. Keep asset provenance/license records. Never describe simulated evidence as real acceptance.
