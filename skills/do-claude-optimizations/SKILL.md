---
name: do-claude-optimizations
description: Memory + CLAUDE.md optimization pass across the entire qagents constellation. Fans out one digester subagent per CLAUDE.md (every subproject + root) plus a memory-index digester and a recall-memo digester — one per roster slug, in parallel — then one sequential cross-cutting digester, merges their digests into a single apply-plan, and trims stale content under both the data write-lock and the dot-claude sentinel. The scheduled/programmatic lane is parked; the standing path is the operator-run interactive variant. Keeps the memory index under the load-truncation cap and every project rule file under its soft size target, which sits deliberately below the warn cap the close gate enforces. Companion to /open, /close, /do-claude-updates.
---

# do-claude-optimizations (alias: `/dco`)

The "shrinking" half of the session-lifecycle skill set. Whereas `/open`,
`/close`, and `/do-claude-updates` add content over time, this skill is the
continuous trim pass that keeps the memory index and every CLAUDE.md below
the harness's load-truncation thresholds.

Contract: the optimization charter (authoritative; the dated spec files it
absorbed are historical). Mechanics live in `scripts/dco.sh`. The subagent
prompts live under `.claude/agents/dco-*`. The programmatic/cron lane is
**parked** alongside the rest of the programmatic-agent lane; the standing
path is the operator-run interactive variant (`dco-manual`), which runs the
same pass via interactive subagent fan-out.

## Procedure

`/dco` (no args) runs from the canonical checkout on `main` with a clean
tree. Same lock-compat refusal as `/do-claude-updates` (no session lock
branches allowed). No worktree — dco operates on `main` directly because
the run is short (~5–15 min) and produces a single commit.

### 1. Pre-flight (mechanical)

`scripts/dco.sh --pre` verifies canonical on main + clean, no session lock
branches, and no pre-existing FAILED marker from a prior run.
`scripts/dco.sh --acquire-sentinel` then atomically creates the data
write-lock followed by the dot-claude sentinel; both held for the entire
run. Exit 13 → a pre-existing FAILED marker; operator investigates first.

### 2. Fan-out (subagents inherit the orchestrator's model)

Spawn the parallel digesters: one `dco-subproject` per subproject, one more
parameterized for the root CLAUDE.md, one `dco-memory` for the memory index +
topic files, and one `dco-memsearch` for the recall daily memos — all in
parallel, one per roster slug. Each writes its digest to a gitignored buffer under
`pending/dco-digests/`; all run in clean contexts.

After the parallel fan-out completes, spawn one sequential `dco-cross`: it
reads every per-sub digest + the cross-cutting memory file list and produces
an authoritative cross-cutting digest resolving per-sub conflicts on shared
memory files.

No digester carries a model pin; the fleet inherits the model the
orchestrator was invoked with, so quota is managed by choosing the
orchestrator's model at invocation.

### 3. Apply (mechanical)

`scripts/dco.sh --apply` copies CLAUDE.md backups aside, applies each
digest's Edit-ready diffs, verifies each post-edit size matches the
digester's predicted size, and commits the canonical tree + the agent-memory
tree separately. On any apply failure it halts at the first failure, writes
a FAILED marker with the apply-plan + failing step, releases both locks, and
exits non-zero.

**Plan-first safety gate — auto-apply is retired.** `--apply` writes a plan
file for review and mutates nothing. Operator workflow: list pending plans,
eyeball the per-section trim counts + any BLOCKED triage rows, then flush
with an explicit `--execute --plan-path <plan>`. On success an `.applied`
sidecar lands (carrying the apply timestamp + commit + backup dir);
re-running on the same plan refuses — the sidecar is the deduplication
contract.

### 4. Release + report (mechanical)

`scripts/dco.sh --release-sentinel` then `--report` releases both sentinels,
emits the uniform footer, and writes the run summary.

## Stop-and-ask cases (only when scripts exit non-zero)

| Exit | Phase | Claude action |
|---|---|---|
| 10 | --pre lock | A session lock branch is present; refuse, list holders, user closes first. |
| 12 | --pre canonical | Canonical not on main or dirty; surface state, user fixes. |
| 13 | --pre queue | Pre-existing FAILED marker; operator investigates before re-firing. |
| 19 | --acquire-sentinel | A sentinel is held; release stale, investigate. |
| 50 | --apply --execute | An Edit call or post-edit size assertion failed mid-run; read the FAILED marker. |
| 51 | --digest / --plan | Malformed digest, a forbidden range-delete indicator, OR a sequential-simulation ambiguity caught BEFORE mutation; operator fixes the digest. |
| 52 | --apply | Target plan already has an `.applied` sidecar; pick a fresh plan. |
| 60 | --digest (SDK) | SDK lane disabled pre-activation; use the manual lane. |
| 61 | --permit-fanout | A required allow-list pattern is missing from settings; update + commit. |
| 20 | any | Unknown error; read log tail, surface. |

## Lock posture

Two sentinels acquired in order: the data write-lock THEN the dot-claude
sentinel. If acquisition of the second fails after the first succeeded, the
script releases the first before exiting — **no partial-lock state ever
persists.** The script does NOT acquire a session-lock branch; it refuses to
fire while any session branch exists (enforced, not advisory).

## What this skill does NOT do

- Does not push to a remote.
- Does not touch any file outside CLAUDE.md + the agent-memory dir.
- Does not modify spec files, subproject plan/memory files, the legal tree,
  source code, tests, or configuration.
- Does not modify git history.
- Does not consume the cross-subproject hint files — that's
  `/do-claude-updates`.
- Does not auto-fire if any session lock branch is present (hard refusal).

## Companions

- `/open <project>` — provisions a worktree.
- `/close [--to-main]` — closes a session.
- `/do-claude-updates` — flushes queued cross-subproject CLAUDE.md hints.
