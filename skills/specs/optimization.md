# Optimization — the charter, condensed

Condensed public-safe rendering of the private optimization charter (the
authoritative contract behind the `do-claude-optimizations` skill body in this
subtree). The dated spec file that preceded the charter is retired; this
render tracks the charter.

## Contract

The optimization pass is the constellation's **continuous shrink pass** over
the always-loaded context surfaces. The session-lifecycle triad writes
content over time; this pass is the counterpart that trims it, keeping each
surface under its load cap so the close-time emergency brake never has to
fire.

Surfaces owned, each with a hard target: the memory index (byte cap primary,
180-line cap secondary), the topic memory files (one-line index hooks,
detail on demand), every per-project rule file (soft line/byte caps with a
floor so trimming cannot hollow a file out), and the recall daily memos
(cold-start injection size; markdown is the source of truth, the vector
index is derived and rebuildable). Everything else is out of bounds — no
spec files, no source code, no legal tree, no append-only archives, no git
history — and the apply tool enforces the boundary at parse time.

## Lane contract

- **The interactive lane is the standing lane.** The main session
  orchestrates the fan-out via subagents, billing the interactive
  subscription; the operator is in the loop at every phase and approves the
  apply.
- **The scheduled/programmatic lane is parked**, fail-closed behind an
  unconditional refusal gate with its schedule entry commented out.
  Restoring it is a future amendment, not a flag flip.
- **Auto-apply is retired.** The apply phase defaults to a dry-run plan;
  every mutation runs under explicit operator approval, and an applied plan
  leaves a sidecar so it cannot be applied twice.

## Fleet shape

A parallel fan-out followed by one sequential agent. In parallel: one digester
per project rule file including the root, plus a memory-index digester and a
recall-memo digester — the roster is the sole owner of that slug set and of its
size, so no consumer pins a count. Then one sequential cross-cutting digester that
adjudicates conflicts on shared memory files — its digest overrides the
others on those files only when its block actually carries an applicable
edit, because dropping a per-project block that holds the only copy of an
edit would destroy it. No digester carries a model pin; the fleet inherits
the model the orchestrator was invoked with.

## License

MIT — see `../../LICENSE-MIT` at the umbrella root.
