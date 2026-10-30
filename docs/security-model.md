# Security and privacy model

## Assets and trust boundaries

Provider credentials, source workspaces, documents/memory, execution permissions, budgets and outputs require protection. Browser content, model output, imported Markdown, external event producers and plugins are untrusted inputs. Running locally does not make a web page or agent-generated command trusted.

## Required controls by milestone

M1: loopback-only API, Host/Origin checks, no outbound network, no host tools, HTML escaping, safe artifact references and separate demo namespace. A task read/preview must not trigger a model call.

M2: provider secrets in server OS credential storage or a deliberately configured environment secret store, never API responses/config exports/telemetry. TLS for remote providers, restricted URL policies, sanitized errors, rate/body limits and explicit timeout budgets. Local endpoints require an intentional local-network grant; defend against SSRF, redirects, DNS rebinding and cloud metadata access.

M3: isolation before tools. Dedicated sandbox identity/container, project-scoped mounted paths, symlink/path traversal defense, bounded CPU/memory/time/output and egress rules. No host home mount, SSH agent or Docker socket by default. Network/model use and tool use have distinct policy gates. External runtime permissions must be known and shown; if they cannot be enforced, observation-only mode is the default.

Approvals bind to action type, exact normalized arguments/hash, project, attempt/fencing token, expiry and requester. The host checks them immediately before execution. A role named “reviewer” cannot approve its own expanded privileges. Changed arguments require a new approval. Expired/duplicate/late approvals cannot revive cancelled work.

M4: notes are data, not instructions. Scoped allowlists, read/write consent, expected revisions, conflict handling and provenance. Never automatically import a full home directory, full conversation history, `.env`, private keys or company data. An imported note cannot grant a new workspace, network access or tool permission.

Remote mode (before any network exposure): authenticated sessions, workspace authorization on every read/command/event/artifact, CSRF/origin protection, TLS and secure cookies. No secrets in URLs or SSE query parameters. A development reverse proxy is not a production auth layer.

## Data and diagnostics

Persist the minimum public activity needed for operational evidence. Do not display or retain private chain-of-thought. Redact known sensitive fields before persistence; pattern matching alone is not sufficient. Users need retention, export and deletion controls. No telemetry by default. Artifact previews must prevent script execution and escape their declared artifact root; downloads include safe content types.

## Abuse cases to test

Malicious note asks to upload secrets; artifact points outside allowed roots; provider URL redirects to metadata IP; stale approval is replayed; two browsers start a task; a timed-out tool actually completed; worker loses lease; external runtime lies about an artifact; model asks to disable its budget; XSS in task/agent names; malicious sprite path; crash between external effect and event append.

Report private security concerns using [SECURITY.md](../SECURITY.md). This document specifies required controls, not an assertion that an unimplemented app is secure.
