# Synthetic examples

`workspace.example.json` illustrates provider/runtime/knowledge configuration with environment variable references, not values. `./local` is a user-created private folder; it is ignored by Git. No path points at a real person's filesystem.

`demo-events.ndjson` describes two mock workers: one produces a synthetic artifact and completes, another waits for an exact approval and is rejected. Event order is deterministic. It is input for the future mock/replay tests, not recorded live activity or proof of a working app.

`config.schema.json` and `event.schema.json` live in [contracts](../contracts/events.md). Actual parsers must validate all typed payloads before persistence. The handoff checker validates the initial example lifecycle only.
