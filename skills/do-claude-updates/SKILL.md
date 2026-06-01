---
name: do-claude-updates
description: Flush queued cross-subproject CLAUDE.md hints from data/claude-updates/*.md into the canonical CLAUDE.mds. Takes a qagents-wide write-lock, reads every CLAUDE.md in the tree for full context, judges each hint, applies/skips edits, deletes consumed hint files, and merges back to main. Run periodically (after several /close cycles); never auto-fired.
---

# do-claude-updates

Mechanical phases live in `scripts/dcu.sh` (`--pre`, `--finish`,
`--report`). This skill is the orchestrator for the *judgment* loop in the
middle. Spec: `open-close-dcu-<date>.md`. Uniform footer at
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
  or a sibling. "Skip with justification" is a valid outcome.
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

`scripts/dcu.sh --finish` verifies the worktree is clean, merges to main
(`--ff-only` then fallback `--no-ff`), unlinks symlinks, then
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

## What this skill does NOT do

- Does not push to a remote.
- Does not touch agent memory (`/close` owns that).
- Does not modify any non-CLAUDE.md file. If a hint suggests code changes,
  mention it in the report and skip.
- Does not consume hints automatically — manual invocation only.
- Does not handle session work — that goes through `/open` + `/close`.

## Companions

- `/open <project>` — provisions a worktree.
- `/close [--to-main]` — closes a session and queues hints.
