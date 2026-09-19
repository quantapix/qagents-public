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
item N, that item must carry retire evidence (a retire through the ledger
verb — in the spool, the session receipts, or the store). The slot file is a
GENERATED render and is never hand-edited; it prunes at `--finish`. The
script scans
`<merge-base>..HEAD` for cites of the form
`(closes|resolves|completes) (next-steps item|ns-item) N(, M)*`
(case-insensitive). The resolution verb is **required**: an earlier form
made it optional, and a commit that merely *mentioned* an item
("next-steps item 41 amended") fired the gate and demanded the item's
deletion. A bare `item N` is rejected for the same reason. If the session
resolved no items, the gate skips with exit 0.

| Exit | Phase | Claude action |
|---|---|---|
| 24 | unknown-cite | A cited item is unknown to the store, the spool, the session receipts AND the rendered slot — a typo'd number, or a slot that has never been rendered. The slot is a GENERATED render: never hand-author or hand-edit it. Check the number against the ledger's list verb; correct a typo in a follow-up commit message; if the item is genuinely new, file it through the ledger's add verb and let `--finish` render it. Re-run. |
| 25 | still-live / slot-drift | Two causes — read the message. **(a) Slot drift, checked first and firing even with zero cites:** a generated slot render was committed on the session branch; revert it and route the change through the ledger verbs. **(b) A cited item is still live** with no retire evidence: retire it through the ledger's resolution verb and confirm by reading it back. Do not delete the item from the file by hand — that act IS cause (a). Survivors are never renumbered; the gaps anchor commit-message audit trails. Re-run. |

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
| 20 | target-dirty | The close-time sweep of cron-fired artifacts at the merge target was refused — in practice by a repo pre-commit hook validating content this session never touched. Read the hook's message in the log tail. Of the three remedies (discard a regenerable artifact, cure the breach, bypass the validator) an agent may take only the first, and only for an artifact it can name as regenerable; the other two are the operator's call. Surface and stop. A green sweep is evidence about that instant only. |
| 24 | next-steps-unknown-cite | See § 5.5's row; the slot is a generated render, never bootstrapped by hand. |
| 25 | next-steps-still-live / slot-drift | A cited item has no retire evidence (retire it through the ledger verb), or a generated render was committed on the branch (revert it) — see § 5.5. Never hand-delete from the render. |

Any other unlisted exit: read the tail of the log, surface.

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
