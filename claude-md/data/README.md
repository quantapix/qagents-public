# claude-md/data/

The shared-hub `CLAUDE.md`s — cross-cutting conventions that no single
subproject owns. These are not subprojects; they describe the *contracts*
between subprojects. See the [claude-md/ README](../README.md) for how to
read the graph, and the [umbrella README](../../README.md) for the broader
thesis.

| File | Mirrors | Kind |
|---|---|---|
| [`data.md`](./data.md) | the shared-data hub charter | data-hub charter |
| [`specs.md`](./specs.md) | the specs convention-anchor | convention-anchor |
| [`tmp.md`](./tmp.md) | the in-flight-proposal convention-anchor | convention-anchor |

Per-subproject `data/<name>/CLAUDE.md` files (a subproject's own data slot,
the status-emit slot) are *not* mirrored here — they're too specific, and
the parent subproject's `CLAUDE.md` already covers them.

## License

MIT — see `../../LICENSE-MIT`. Prose + AI-agentic workflow files fall under
the MIT side of the two-license pair.
