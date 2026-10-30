# Provider and runtime adapters

## What “any provider” means

A stable port plus a documented registration/conformance path allows a provider to be added without changing the office or business rules. Providers have different protocols, models, entitlements and capabilities. An adapter is supported only after its conformance tests and real opt-in acceptance pass; a matching HTTP URL does not prove full compatibility.

Do not assume a ChatGPT, Copilot, Claude or other end-user subscription grants API access or permits using undocumented tokens. Accept only officially supported credentials/auth flows and disclose per-provider requirements during setup.

## ModelProvider contract (reference, not implemented)

```ts
interface ModelProvider {
  readonly id: string;
  capabilities(connection: ConnectionRef): Promise<ModelCapabilities>;
  stream(request: NormalizedRequest, context: {
    secrets: SecretResolver;
    signal: AbortSignal;
    remainingBudget: Budget;
  }): AsyncIterable<ModelEvent>;
}
```

`NormalizedRequest`: model ID (user configured), public system/task messages, supported image/tool definitions, output/token caps, request ID. Preserve tool call IDs and structured errors. Never concatenate model-generated arguments into a shell command. `ModelEvent`: text delta, tool-call proposal, reported usage, sanitized error, completion. A model completion only ends inference, not the task.

Capabilities include streaming, tool calls, structured output, images, cancellation and reported usage/cost. Do not silently remove a required capability. Cancellation that only stops local listening must not be advertised as remote execution cancellation.

## AgentRuntime contract (reference, not implemented)

```ts
interface AgentRuntime {
  readonly id: string;
  capabilities(): RuntimeCapabilities;
  start(input: StartAttempt): Promise<RuntimeSessionRef>;
  observe(session: RuntimeSessionRef, after?: string): AsyncIterable<RuntimeEvent>;
  cancel(session: RuntimeSessionRef, requestId: string): Promise<CancelReceipt>;
  reconcile(session: RuntimeSessionRef): Promise<RuntimeSnapshot>;
}
```

Optional approve/pause/resume methods are capability gated and normalize acknowledgement states. An observed external session cannot be controlled unless the runtime actually provides a supported control API. `CancelReceipt` distinguishes request accepted, already terminal, unsupported and unknown. A transport timeout is not confirmed cancellation.

The built-in runtime, when implemented, orchestrates provider messages and bounded tools. External adapters (e.g. Hermes or an official CLI/SDK) observe/control external runtimes; they do not scrape terminal text to invent progress or reach into personal credential stores. Treat ACP/MCP support as explicit protocol/version capabilities: MCP tools alone do not supply a session lifecycle or execution sandbox.

## Initial matrix and delivery order

| Adapter | Kind | Planned milestone | Current support |
|---|---|---|---|
| Deterministic mock | Runtime + model fixture | M1 | Specified, not implemented |
| Configurable OpenAI-compatible HTTP | Model | M2 | Specified; protocol subset must be documented |
| Anthropic native protocol | Model | M2 | Specified; verify official API at implementation |
| Local model endpoint | Model | M2 | Through an adapter; not a separate automatic guarantee |
| Built-in bounded tools | Execution runtime | M3 | Requires sandbox and host policy |
| Hermes | External runtime | After core conformance | Optional, unimplemented |
| Codex / Claude Code / Copilot | External runtimes | Future adapters | Official interfaces/auth must be evaluated individually |
| Markdown / Obsidian vault | Memory | M4 | Optional; no Obsidian process dependency |

M2 is accepted only when two distinct model protocols pass the same contract fixtures, and credentialed integrations are explicitly opt-in. Mocked protocol tests are not real external acceptance. Start with configurable IDs; never ship a hardcoded “best/current” model.

## Adapter conformance checklist

Input/output validation; stream ordering; malformed/truncated responses; tool-call fragments and IDs; unsupported capability rejection; bounded retries/429/Retry-After; timeout/abort; redacted errors; unknown usage; budget reservation/release; duplicate/out-of-order runtime events; reconnect/reconcile; cancellation race; no credentials in logs or browser payloads. Record protocol/version and acceptance date in the support matrix when an adapter is implemented.
