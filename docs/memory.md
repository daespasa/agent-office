# Project knowledge and optional Obsidian

## Portable by default

Use a scoped plain-Markdown store through `MemoryStore`; Obsidian is an optional editor/viewer for the same files, never a runtime requirement. No repository-specific home path, installed plugin, API key or proprietary cloud sync is assumed.

A suggested user-owned vault layout is `Projects/<stable-project-id>/{State,Decisions,Knowledge,Sessions}`. Agent Office configuration references a project root and its explicitly granted memory subfolder; the public repository contains only synthetic examples.

## Operations

`search(scope, query, limit)` returns bounded snippets and source refs; `read(ref)` returns text plus revision/hash and provenance; `proposeWrite` prepares a curated diff; `commitWrite(expectedRevision)` atomically writes or returns a conflict. Adapters must preserve manual edits and arbitrary user frontmatter they do not own.

The agent reads a short project State and only relevant sources at the start of substantive work. At close it proposes a concise summary: objective, result, evidence, uncertainty and next step. Automatic hook activity is metadata, not a verified semantic summary. Full transcript ingestion is off by default and outside the initial scope.

Repository docs remain authoritative for versioned code/architecture decisions. Imported mirrors state their origin, branch/commit where applicable, sync time and stale/missing status. A source disappearing on a different branch does not justify deleting historical knowledge.

## Conflicts and trust

Do not overwrite a file with a different expected hash. Preserve a conflict copy and show a review action. Scope checks include realpath/symlink handling and deny traversal out of the granted root. Sanitize previews; do not execute embedded code, URLs or commands from notes. Optional indexing must be local, rebuildable and clearly separated from canonical Markdown.

Project knowledge cannot authorize deployment or contact with another person. An old successful operation is not a standing instruction to repeat it. Every note distinguishes requirement, hypothesis and dated observation. See [security model](security-model.md).
