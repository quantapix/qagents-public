---
name: open
description: Start a new Claude Code session by creating a git branch + worktree for a qagents project (whole-repo or subproject). The branch is the write-lock; subsequent opens of the same project stack as numbered branches off their predecessor. Use whenever the user begins parallel work; ends with `/close`.
---

# open

Provision a write-locked session for a qagents project. Companion to
`/close` and `/do-claude-updates`.

Contract: the session-lifecycle charter (authoritative — condensed render at
`specs/session-lifecycle.md`; the open phases + the next-steps mandate + the
zero-prompt allow-list).
Mechanics live in `scripts/open.sh`; the uniform footer in
`scripts/lib/footer.sh`.

## Procedure

`/open <project>` runs exactly one command (`scripts/open.sh <project>`),
which does all of: validate the project, classify any canonical dirty state
(sweep state-checkpoint files, refuse on real work), warn on stale
`pending/` and a stale write-lock, refuse on lock-conflict, compute branch +
parent (stacking via the smallest free `<project>-N`), create the branch +
worktree off the parent, symlink the venv and applicable env files, hydrate
`node_modules` if a workspace member, **briefing-read of the project's
`next-steps` slot** (rendered as the footer's Outstanding rows; an absent
slot falls back to `(none)`; a whole-repo open reads only the whole-repo
slot — context-bloat prevention), and print the entry forms. Full log
under `pending/logs/`.

Surface the script's stdout — the `ok branch=… parent=… wt=…` line, the
"To enter the session" block, and the uniform `<project> open complete`
footer block including the Outstanding table — and stop. The entry block
carries **three** forms: a CLI form (`cd … && claude`), a desktop-app form
(open the printed project folder as a local session), and a
terminal-multiplexer form that adopts the provisioned worktree as a
workspace. Pass all three through verbatim; the user picks the surface. A
multiplexer workspace is a *view* of the session, never a lock — the branch
stays the only write-lock — and the desktop app must open the provisioned
folder as-is rather than minting its own worktree. The footer is also
persisted under `data/summaries/open/`.

The Outstanding rows are the candidate session agenda: section A (ready
now) is highest priority; section B (gated on external) blocks unless the
gate cleared. There is no third section — cross-cutting items live in the
owning project's own slot, and recurring ones surface as ledger rows
against their owner. To preview just the briefing read without
provisioning a worktree: `scripts/open.sh --next-steps <project>`.

## Valid `<project>`

`qagents` (whole-repo) or one of the subproject slugs.

## Locking model (recap)

- The branch named exactly `<project>` (or `<project>-N`) IS the write-lock.
- `/open qagents` while any subproject lock exists → exit 10 with the
  conflicting branch list.
- `/open <subproject>` while any `qagents`/`qagents-N` exists → same.
- `/open <project>` when `<project>` exists → the script stacks on
  `<project>-N`.

## Stop-and-ask cases (script exits non-zero on each)

| Exit | Meaning | What Claude does |
|---|---|---|
| 10 | Lock conflict | Surface the conflicting branches; ask how to proceed. |
| 11 | Unknown project | Show the valid set; ask. |
| 12 | Real dirty state in canonical | Show the dirty paths; ask to commit/stash. Do NOT auto-sweep. |
| 13 | Not a git repo | Configuration problem; surface and stop. |
| 20 | Unknown error | Read the tail of the open log; surface. |

On exit 0 the script has printed the three entry forms — pass them through
verbatim.

## What this skill does NOT do

- Never pushes, and never makes a standalone administrative commit on
  `main`. The script does make two commits: a state-checkpoint sweep on
  `main` only when canonical carries pure cron/checkpoint dirty state, and
  the open-summary on the *session branch*.
- Does not delete or modify existing branches.
- Does not touch the dot-claude sentinel (that's `/close`'s job).
- Does not do anything the script doesn't — the script is the source of
  truth.

## Companions

- `/close [--to-main]` — closes the worktree and merges.
- `/do-claude-updates` — flushes queued cross-subproject CLAUDE.md hints.
