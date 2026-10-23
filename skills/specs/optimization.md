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

- **The interactive lane is the standing lane by design;** the main
  session orchestrates the fan-out via subagents; the operator is in the
  loop at every phase and approves the apply.
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

## Relocation review

The pass carries its own counterweight. Before a capped surface is trimmed,
its content is spread down the disclosure ladder (always loaded, loaded per
open, loaded on demand) and never discarded into history alone. The review
half runs inside the pass when one of a fixed set of trigger arms fires,
among them the memory index nearing its cap, a rule-file over or approaching
a cap, owed review items, and a long gap since the last review. It writes a
blueprint with an aging register and an apply prompt, and files a routing
item. The moves themselves run in one separate whole-repo session, after the
operator rules on the blueprint's priority items. That session's apply log
takes one item per row, with a disposition from a closed set: cured,
consumed, owner-done, struck or dropped. The first three must cite a commit
or the row keeps aging. Work left unconsumed escalates after two later
passes, or by one interval per seven days when no pass runs.

## License

MIT — see `../../LICENSE-MIT` at the umbrella root.
