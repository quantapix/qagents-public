---
name: do-claude-updates
description: Flush queued cross-subproject CLAUDE.md hints from data/claude-updates/*.md into the canonical CLAUDE.mds. Takes a qagents-wide write-lock, reads every CLAUDE.md in the tree for full context, judges each hint, applies/skips edits, deletes consumed hint files, and merges back to main. Run periodically (after several /close cycles); never auto-fired.
---

# do-claude-updates

Mechanical phases live in `scripts/dcu.sh` (`--pre`, `--finish`,
`--report`). This skill is the orchestrator for the *judgment* loop in the
middle. Contract: the session-lifecycle charter (condensed render at
`specs/session-lifecycle.md`). Uniform footer at
`scripts/lib/footer.sh` writes under `data/summaries/dcu/`.

## Procedure

`/do-claude-updates` (no args) runs from the canonical checkout on `main`
with a clean tree.

### 1. Pre-flight + provision worktree (mechanical)

`scripts/dcu.sh --pre` verifies canonical is on main + clean, the hint queue
is non-empty, and no session lock branches exist, then provisions a
dedicated worktree with the venv + applicable env symlinks. Output includes
the worktree path and the queue size. Exit 13 → queue empty, clean exit;
other non-zero → see the table below.

### 2. Load full CLAUDE.md context (judgment)

Read every CLAUDE.md in the worktree (excluding `node_modules` / venv).
**Note size at read time** (line + byte count); files near the soft cap are
"near the cap" — prefer trim/consolidate over additive growth on those when
applying edits.

### 3. Process each hint file (judgment)

For each hint file in `data/claude-updates/`:

- Read its contents.
- With every CLAUDE.md in view, decide what (if anything) to apply where.
  The same hint may translate to zero, one, or several edits; it may be
  obsolete (later sessions covered it) — skip; it may cascade into the root
  or a sibling. An actionable hint that is not a `CLAUDE.md` edit is
  **routed, not dropped**: it becomes a next-steps item for the owning
  project through the ledger's add verb (never an edit to the generated slot
  render). "Skip with justification" remains a valid outcome.
- **Apply edits surgically** — preserve unrelated content; when the target
  is near the cap, trim adjacent stale content as part of the edit so net
  size doesn't grow.
- **Delete the consumed hint file** regardless of whether it produced edits
  — "consumed" means "reviewed in full context", not "applied".
- Stage + commit the changes for this hint with a message naming the source
  branch and listing applied paths (or `no edits applied; <reason>`).

If a hint file is **malformed** (unparseable, or asserts something
demonstrably false): leave it on disk, surface it in the report, continue.

### 4. Merge + teardown (mechanical)

`scripts/dcu.sh --finish` verifies the worktree is clean, **refuses if the
merge range touches an out-of-scope path** (only `CLAUDE.md` files, the hint
queue, and the dcu run summaries may ride the lane — exit 23), refuses a run
that grows a `CLAUDE.md` to or past the close gate's fail cap (exit 24),
merges to main (`--ff-only` then fallback `--no-ff`), unlinks symlinks, then
`worktree remove` + `branch -d` + `prune`, and emits the uniform footer.

### 5. Report

Hint files consumed; applied / skipped (with reasons); CLAUDE.md paths
edited; sizes before → after for any that gained or lost content; commits
created; any malformed hint files left on disk.

## Stop-and-ask cases (only when scripts exit non-zero)

| Exit | Phase | Claude action |
|---|---|---|
| 10 | --pre lock | A session lock branch is present; refuse, list holders, user closes first. |
| 12 | --pre canonical | Canonical not on main or dirty; surface state, user fixes. |
| 13 | --pre queue | Queue empty; clean exit. |
| 17 | --finish merge | Merge conflict back to main (shouldn't happen given the lock); leave state, user resolves. |
| 20 | any | Unknown error; read log tail, surface. |
| 21 | --abort | A crashed prior run's worktree still holds work; inspect it, then `--finish` to land it or force-discard after inspection. |
| 23 | --finish scope | The merge range touches an out-of-scope path (next-steps slots are generated renders — route the hint through the ledger verb instead); a stray write slipped onto the dcu branch — inspect and relocate it, don't merge. |
| 24 | --finish size | A touched `CLAUDE.md` would land at or over the close gate's fail cap **and this run grew it** — past that size the owning scope's own close refuses for growth it did not author. Trim it on the dcu branch or drop the hint with a stated disposition, then re-run `--finish`. No override. A run that does not grow an already-oversized file passes by design — refusing the trim would be refusing the cure. |
| 25 | --finish / inflow grade | Inflow rung: a write grows a `CLAUDE.md` into the soft band with no hot-rule commit trailer, or into the warn band (no override). Offset it with a trim in the same commit, demote the rule to a home the refusal lists, or — soft band only, for a genuinely hot rule — carry the trailer. A file the run nets ≤ 0 is exempt. |
| 26 | --finish / inflow grade | The write's added text already lives in a demotion home the target file points to. Replace the restatement with a pointer, or drop it. No override. |

## What this skill does NOT do

- Does not push to a remote.
- Does not touch agent memory (`/close` owns that).
- Modifies only `CLAUDE.md` files. A hint suggesting a code, spec, test or
  data change is captured as a next-steps item for the owning session
  through the ledger verb — never applied here, never silently skipped.
- Does not consume hints automatically — manual invocation only.
- Does not handle session work — that goes through `/open` + `/close`.

## Companions

- `/open <project>` — provisions a worktree.
- `/close [--to-main]` — closes a session and queues hints.
