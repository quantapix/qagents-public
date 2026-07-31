---
name: close
description: End a Claude Code session by summarizing the session, updating memories under the agent-memory dir, applying immediate-context CLAUDE.md edits, queuing broader-cascade hints, and merging the session's branch into its stack parent (or all the way to main with --to-main). Companion to `/open`. Use whenever a session is complete.
---

# close

Mechanical phases live in `scripts/close.sh` (subcommands `--noop-check`,
`--pre`, `--commit`, `--status-emit`, `--next-steps`, `--finish`,
`--resume-after-stash-pop`, `--verify`, `--footer`). This skill is the
orchestrator that interleaves the *judgment* steps only an LLM in session
context can do. Contract: the session-lifecycle charter (condensed render at
`specs/session-lifecycle.md` — the close phases + the noop short-circuit +
the per-hop cascade footer + the next-steps gate + the canonical-edit hook)
+ the close-time status-emit contract. Uniform footer
at `scripts/lib/footer.sh` emits to stdout AND appends under
`data/summaries/close/`.

## Bash discipline (MUST — these are contracts, not advisories)

These rules eliminate a permission-prompt storm. Failing any of them
re-introduces prompts even with a fully populated allow-list.

- **MUST use the absolute literal path to `close.sh`** for every
  invocation. Never a relative form — each path form requires a separate
  matcher in the settings allow-list.
- **MUST NOT use compound bash** — no `&&`, `||`, `;`, or `|`. That
  includes piping output to `tail`. Read the log file via the Read tool
  instead.
- **MUST NOT `cd <abs-path> && git …`** — trips a hardcoded
  foreign-directory security prompt that allow-listing can't silence. Use
  `git -C <abs-path> …` as a standalone command.
- **MUST NOT re-verify with raw git after `--pre` ran** — `--pre` already
  wrote the diff and commit list to its log; Read the log file.
- **Temp files belong in-repo** under `<worktree>/pending/tmp/`
  (gitignored). The OS `/tmp/` is outside the allowed write boundary.

`<repo>` = the canonical repo root (source of `close.sh`). `<worktree>` =
the worktree root for the active branch. `<sub>` = the subproject slug.
Resolve these to literal absolute paths before issuing tool calls.

## Procedure

`/close [<branch>] [--to-main]` runs in this exact sequence. Default
`<branch>` = current branch.

### 0. Noop short-circuit (mechanical)

`close.sh --noop-check <branch>`:

- **exit 0 (noop)** — the branch has zero commits ahead of target AND the
  worktree is clean. **Skip Phases 1–6 entirely**; jump to Phase 7
  (`--finish`) + Phase 8 (`--verify`). No summary, no memory edits, no
  CLAUDE.md edits, no status emit, no commit — the footer `--finish` writes
  IS the entire close artifact.
- **exit 1 (work present)** — proceed with Phase 1.

### 1. Pre-flight (mechanical)

`close.sh --pre <branch>`: resolves the worktree, runs the stack-top check,
classifies dirty state on both sides (sweeps cron-fired artifacts, refuses
on real work), inspects what's being merged (commits + diffstat to the log),
runs hub-overlap + cross-subproject scans, runs the gitignored-binary rescue
scan, and runs the CLAUDE.md size check on every CLAUDE.md the merge
touches. Exit 0 → proceed; non-zero → handle per the table below.

### 2. Write the session summary (judgment)

Save under `data/summaries/close/` (local time, minute precision; never
overwrite). Synthesize what was done, why, and what was learned — not a
transcript. The mechanical footer table is appended below your narrative by
`--finish` at Phase 7.

### 3. Update agent memory (judgment)

Acquire the dot-claude sentinel via `close.sh --acquire-sentinel <branch>`
(atomic, exits 19 if held). Update memories per the memory-index discipline
in the root `CLAUDE.md`: write/refine/prune topic files, keep index entries
one line under the cap. **Watch the memory index size** — it truncates
around a fixed line count at session start; consolidate before adding when
near the cap. Write the commit message to an in-repo temp file, then
`close.sh --commit-memory <msgfile>` (asserts the sentinel is held, commits
against the agent-memory dir, releases the sentinel on success or failure).

### 4. Update CLAUDE.md files (judgment, two paths)

**4a. Immediate-context.** Re-read every CLAUDE.md the session touched;
fix stale phrasings at close where you have full session context. Edit the
project's own CLAUDE.md (and the root only for genuinely cross-cutting
changes). **Size discipline:** warn near the soft cap, fail at the hard cap;
prefer trim/consolidate over additive growth.

**4b. Broader-cascade hints.** If the session's learnings *might* affect
sibling CLAUDE.mds or the root, write a free-form hint file under
`data/claude-updates/` (hints not commands). Skip entirely if there are no
broader hints — do not write empty files.

### 5. Mandatory status emit (mechanical)

`close.sh --status-emit <branch>` regenerates the subproject's status-hub
slot. Whole-repo closes fan out via the status orchestrator.

| Exit | Phase | Claude action |
|---|---|---|
| 42 | producer-failed | Surface stderr; fix the producer (or queue the failure as a known-issue note). |
| 43 | no-producer | No `scripts/status_emit.*` AND no opt-out comment; author a minimal producer OR add the opt-out comment. |
| 44 | schema-fail | Producer regressed; fix the emit before continuing. |

### 5.5. Mandatory next-steps gate (mechanical)

`close.sh --next-steps <branch>` enforces the forward-only rule for the
project's `next-steps` slot: when commit messages in the merge range cite
item N, that item must be deleted from the slot file. The script scans
`<merge-base>..HEAD` for cites of the form
`(closes|resolves|completes)? (next-steps item|ns-item) N(, M)*`
(case-insensitive); bare `item N` is rejected. If the session resolved no
items, the gate skips with exit 0.

| Exit | Phase | Claude action |
|---|---|---|
| 24 | missing-slot-file | Cites items but the slot file doesn't exist. Bootstrap from the slot template; list cited items; delete the just-cited ones; re-stage; re-run. |
| 25 | items-not-deleted | Cited items still present. Delete each (do NOT renumber survivors — gaps anchor commit-message audit trails); re-stage; re-run. |

### 6. Commit session work (judgment writes the message)

Write the commit message to an in-repo temp file, then `close.sh --commit
<branch> <msgfile>`. Returns "ok nothing-to-commit" if already clean.

### 7. Merge + teardown (mechanical)

`close.sh --finish <branch>` (add `--to-main` to cascade through the
stack): the memsearch stash dance (only if needed), `--ff-only` then
fallback `--no-ff`, auto-resolves memsearch-only conflicts to the richer
side, pre-cleans worktree memsearch state, unlinks symlinks, then
`worktree remove` + `branch -d` + `prune`. With `--to-main`, cascades up the
stack repeating merge+teardown at each level, with a silent per-hop summary
at each level.

### 8. Verify + report

`close.sh --verify <target>` (= `main` after `--to-main`, else the parent)
prints the last commit on target, the branch list, the worktree list, and
an orphan-dir scan. Surface the uniform `<project> close complete` footer +
the `--verify` output verbatim as the close report.

## Stop-and-ask cases (only when the script exits non-zero)

| Exit | Phase | Claude action |
|---|---|---|
| 10 | stack-top | Child branch exists; close the child first. |
| 11 | resolve | Not a worktree-managed lock branch; surface and stop. |
| 12 | dirty-classify | Real uncommitted work on either side; show paths; user commits/stashes. |
| 13 | hub-overlap | HIGH-risk parallel writes to a shared-write hub; show parallel commits; user decides. |
| 14 | cross-subproject | Subproject branch wrote outside its scope; user confirms intent. |
| 15 | rescue | Non-trivial gitignored binaries about to be wiped; rescue / accept loss / discard. Default: rescue. |
| 16 | claude-md-size | A CLAUDE.md in the diff exceeds the hard cap; trim before re-running. |
| 17 | merge | Conflict on a non-memsearch path; leave state; user resolves. |
| 18 | stash-pop | Memsearch stash-pop conflict with unique content on both sides; do a union resolution by hand, commit, then `--resume-after-stash-pop`. |
| 19 | sentinel | dot-claude sentinel already held (likely a crashed prior close); investigate. |
| 21 | branch-d | `git branch -d` refused (not fully merged); investigate. |
| 22 | commit-memory | `--commit-memory` called without sentinel held — acquire it first. |
| 24 | next-steps-missing | Cites items but the slot file doesn't exist; bootstrap from the template. |
| 25 | next-steps-not-deleted | Cited items still present; delete them (no renumbering). |

Any other exit (20): read the tail of the log, surface.

## What this skill does NOT do

- Does not push to a remote.
- Does not squash.
- Does not auto-resolve conflicts on shared-write paths (only memsearch-only
  conflicts auto-resolve).
- Does not delete schedules or hooks.
- Does not consume the cross-subproject hint files — that's
  `/do-claude-updates`.

## Companions

- `/open <project>` — provisions a worktree.
- `/do-claude-updates` — flushes queued cross-subproject hints in
  full-tree context.
